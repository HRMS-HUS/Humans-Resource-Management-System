from sqlalchemy.ext.asyncio import AsyncSession
from ..models import application as models
from ..schemas import application as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock
from ..services import users as user_service  # Add this import

class DatabaseOperationError(Exception):
    pass

async def _validate_user_exists(db: AsyncSession, user_id: str):
    """Validate if a user exists in the database"""
    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly
        raise http_exc
    except Exception as e:
        # Log the actual error here if needed
        print(f"Error validating user: {str(e)}")  # For debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error while validating user: {str(e)}"
        )

async def create_application(db: AsyncSession, application: schemas.ApplicationCreate):
    # Validate user existence
    await _validate_user_exists(db, application.user_id)
    
    async with DistributedLock(f"application:user:{application.user_id}"):
        try:
            db_application = models.Application(
                user_id=application.user_id,
                leave_type=application.leave_type,
                reason=application.reason,
                start_date=application.start_date,
                end_date=application.end_date,
                status="Pending"
            )
            db.add(db_application)
            await db.commit()
            await db.refresh(db_application)
            return db_application
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

async def get_application_by_id(db: AsyncSession, application_id: str):
    try:
        result = await db.execute(
            select(models.Application).filter(
                models.Application.application_id == application_id
            )
        )
        application = result.scalar_one_or_none()

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        return application
    except HTTPException:
        raise

async def get_applications_by_user_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.Application).filter(
                models.Application.user_id == user_id
            )
        )
        applications = result.scalars().all()

        if not applications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No applications found for this user"
            )
        return applications
    except HTTPException:
        raise

async def get_all_applications(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Application]:
    result = await db.execute(
        select(models.Application).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_application(
    db: AsyncSession, application_id: str, application: schemas.ApplicationUpdate
):
    async with DistributedLock(f"application:{application_id}"):
        try:
            query = (
                update(models.Application)
                .where(models.Application.application_id == application_id)
                .values(application.dict(exclude_unset=True))
            )

            result = await db.execute(query)
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            return await get_application_by_id(db, application_id)
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def delete_application(db: AsyncSession, application_id: str):
    async with DistributedLock(f"application:{application_id}"):
        try:
            result = await db.execute(
                delete(models.Application).where(
                    models.Application.application_id == application_id
                )
            )
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            return {"message": "Application deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
