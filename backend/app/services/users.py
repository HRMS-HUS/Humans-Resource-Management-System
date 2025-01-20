from sqlalchemy.ext.asyncio import AsyncSession
from ..configs.database import get_db
from ..models import users as models
from ..schemas import users as schemas
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, and_, func, text, delete, update
from ..utils import crypto, jwt
from ..services import authentication
from typing import Optional, List
from ..utils.logger import logger

class DatabaseOperationError(Exception):
    pass

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    try:
        db_user = models.Users(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        await logger.info("Created user", {
            "user_id": db_user.user_id,
            "username": user.username,
            "role": user.role
        })
        return db_user
    except Exception as e:
        await logger.error("Create user failed", error=e)
        await db.rollback()
        raise

async def get_user_by_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(select(models.Users).filter_by(user_id=user_id))
        user = result.scalar_one_or_none()
        if user:
            await logger.info("Retrieved user by id", {"user_id": user_id})
        else:
            await logger.warning("User not found", {"user_id": user_id})
        return user
    except Exception as e:
        await logger.error("Get user by id failed", {"user_id": user_id, "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def update_user(db: AsyncSession, user_id: str, user_update: schemas.UserUpdate):
    try:
        # Check if user exists
        existing_user = await get_user_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Initialize update data dictionary
        update_data = {}

        # Username validation and update
        if user_update.username is not None:
            # if len(user_update.username.strip()) < 3:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Username must be at least 3 characters long"
            #     )
            
            # Check if username already exists
            username_check = await db.execute(
                select(models.Users)
                .filter(models.Users.username == user_update.username)
                .filter(models.Users.user_id != user_id)
            )
            if username_check.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            update_data["username"] = user_update.username.strip()

        # Password validation and update
        if user_update.password is not None:
            # if len(user_update.password) < 6:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Password must be at least 6 characters long"
            #     )
            update_data["password"] = crypto.hash_password(user_update.password)

        # Role and status update
        if user_update.role is not None:
            update_data["role"] = user_update.role
        if user_update.status is not None:
            update_data["status"] = user_update.status

        # Only update if there are changes
        if update_data:
            stmt = (
                update(models.Users)
                .where(models.Users.user_id == user_id)
                .values(**update_data)
            )
            await db.execute(stmt)
            await db.commit()
            
            # Refresh user data
            await db.refresh(existing_user)
            
            # Log the update, excluding password from logs
            log_data = {k: v for k, v in update_data.items() if k != "password"}
            await logger.info("Updated user", {
                "user_id": user_id,
                "updates": log_data
            })

        return existing_user
        
    except HTTPException as he:
        await logger.warning("Update user validation failed", {
            "user_id": user_id,
            "error": he.detail
        })
        raise
    except Exception as e:
        await logger.error("Update user failed", {
            "user_id": user_id,
            "error": str(e)
        })
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

async def change_own_password(
    db: AsyncSession, 
    user: models.Users,  # Pass the user object directly
    current_password: str, 
    new_password: str
):
    try:
        # Verify current password
        if not crypto.verify_password(current_password, user.password):
            await logger.warning("Invalid current password", {"user_id": user.user_id})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        # Hash and update new password
        hashed_password = crypto.hash_password(new_password)
        stmt = (
            update(models.Users)
            .where(models.Users.user_id == user.user_id)
            .values(password=hashed_password)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(user)
        await logger.info("Changed own password", {"user_id": user.user_id})
        
        return user
    except Exception as e:
        await logger.error("Change password failed", {"user_id": user.user_id, "error": str(e)})
        await db.rollback()
        raise

async def admin_change_password(
    db: AsyncSession, 
    user_id: str, 
    new_password: str
):
    try:
        user = await get_user_by_id(db, user_id)
        
        # Hash and update password
        hashed_password = crypto.hash_password(new_password)
        stmt = (
            update(models.Users)
            .where(models.Users.user_id == user_id)
            .values(password=hashed_password)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(user)
        await logger.info("Admin changed user password", {"user_id": user_id})
        
        return user
    except Exception as e:
        await logger.error("Admin change password failed", {"user_id": user_id, "error": str(e)})
        await db.rollback()
        raise

async def delete_user(db: AsyncSession, user_id: str):
    try:
        await get_user_by_id(db, user_id)
        
        
        stmt = delete(models.Users).where(models.Users.user_id == user_id)
        result = await db.execute(stmt)
        await db.commit()
        await logger.info("Deleted user", {"user_id": user_id})
        
        return {"detail": "User deleted successfully"}
    except Exception as e:
        await logger.error("Delete user failed", {"user_id": user_id, "error": str(e)})
        await db.rollback()
        raise


async def get_all_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10, 
    role: Optional[models.RoleEnum] = None, 
    status: Optional[models.StatusEnum] = None
) -> List[models.Users]:
    try:
        # Create base query
        query = select(models.Users)
        
        if role is not None:
            query = query.filter(models.Users.role == role)
        
        if status is not None:
            query = query.filter(models.Users.status == status)
        
        # Add ordering by user_id as integer
        query = query.order_by(text("CAST(user_id AS INTEGER)"))
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        users = result.scalars().all()
        
        await logger.info("Retrieved all users", {
            "count": len(users),
            "skip": skip,
            "limit": limit,
            "role": str(role) if role else None,
            "status": str(status) if status else None
        })
        
        return users if users else []
    except Exception as e:
        await logger.error("Get all users failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def count_users(
    db: AsyncSession, 
    role: Optional[models.RoleEnum] = None, 
    status: Optional[models.StatusEnum] = None
) -> int:
    try:
        query = select(func.count(models.Users.user_id))
        
        if role is not None:
            query = query.filter(models.Users.role == role)
        
        if status is not None:
            query = query.filter(models.Users.status == status)
        
        result = await db.execute(query)
        count = result.scalar_one()
        
        await logger.info("Counted users", {
            "count": count,
            "role": str(role) if role else None,
            "status": str(status) if status else None
        })
        
        return count
    except Exception as e:
        await logger.error("Count users failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )