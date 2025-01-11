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
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def update_user(db: AsyncSession, user_id: str, user_update: schemas.UserUpdate):
    try:
        existing_user = await get_user_by_id(db, user_id)
        
        if user_update.username:
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
            
            update_data = {"username": user_update.username}
            
            if user_update.role is not None:
                update_data["role"] = user_update.role
            if user_update.status is not None:
                update_data["status"] = user_update.status
                
            stmt = (
                update(models.Users)
                .where(models.Users.user_id == user_id)
                .values(**update_data)
            )
            await db.execute(stmt)
            await db.commit()
            await db.refresh(existing_user)
        
        return existing_user
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
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
        
        return user
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

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
        
        return user
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def delete_user(db: AsyncSession, user_id: str):
    try:
        await get_user_by_id(db, user_id)
        
        
        stmt = delete(models.Users).where(models.Users.user_id == user_id)
        result = await db.execute(stmt)
        await db.commit()
        
        return {"detail": "User deleted successfully"}
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(jwt.oauth2_scheme)):
#     return await jwt.get_current_user(token, db)

# async def get_active_user(db: AsyncSession = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
#     if current_user.status != models.StatusEnum.Active:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
#     return current_user

# async def get_current_admin(db: AsyncSession = Depends(get_db), current_user: models.Users = Depends(get_active_user)):
#     if current_user.role != models.RoleEnum.Admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#     return current_user

async def get_all_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10, 
    role: Optional[models.RoleEnum] = None, 
    status: Optional[models.StatusEnum] = None
) -> List[models.Users]:
    try:
        query = select(models.Users)
        
        
        if role is not None:
            query = query.filter(models.Users.role == role)
        
        
        if status is not None:
            query = query.filter(models.Users.status == status)
        
        
        query = query.offset(skip).limit(limit)
        
        
        result = await db.execute(query)
        users = result.scalars().all()
        
        return users if users else []
    except Exception:
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
        return result.scalar_one()
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )