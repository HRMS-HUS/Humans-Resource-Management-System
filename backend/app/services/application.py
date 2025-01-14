from sqlalchemy.ext.asyncio import AsyncSession
from ..models import application as models
from ..schemas import application as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock
from ..services import users as user_service  # Add this import
from ..utils.logger import logger

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
            await logger.info("Created application", {
                "application_id": db_application.application_id,
                "user_id": application.user_id
            })
            return db_application
        except Exception as e:
            await logger.error("Create application failed", error=e)
            await db.rollback()
            raise

async def get_application_by_id(db: AsyncSession, application_id: str):
    try:
        result = await db.execute(
            select(models.Application).filter(
                models.Application.application_id == application_id
            )
        )
        application = result.scalar_one_or_none()

        if not application:
            await logger.warning("Application not found", {"application_id": application_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        await logger.info("Retrieved application", {"application_id": application_id})
        return application
    except Exception as e:
        await logger.error("Get application by id failed", error=e)
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
            await logger.warning("No applications found", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No applications found for this user"
            )
        await logger.info("Retrieved applications for user", {"user_id": user_id, "count": len(applications)})
        return applications
    except Exception as e:
        await logger.error("Get applications by user failed", error=e)
        raise

async def get_all_applications(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Application]:
    try:
        result = await db.execute(
            select(models.Application).offset(skip).limit(limit)
        )
        applications = result.scalars().all()
        await logger.info("Retrieved all applications", {"count": len(applications), "skip": skip, "limit": limit})
        return applications if applications else []
    except Exception as e:
        await logger.error("Get all applications failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

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
                await logger.warning("Application not found for update", {"application_id": application_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            updated_app = await get_application_by_id(db, application_id)
            await logger.info("Updated application", {
                "application_id": application_id,
                "new_status": updated_app.status
            })
            return updated_app
        except Exception as e:
            await logger.error("Update application failed", {"application_id": application_id, "error": str(e)})
            await db.rollback()
            raise

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
                await logger.warning("Application not found for deletion", {"application_id": application_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            await logger.info("Deleted application", {"application_id": application_id})
            return {"message": "Application deleted successfully"}
        except Exception as e:
            await logger.error("Delete application failed", {"application_id": application_id, "error": str(e)})
            await db.rollback()
            raise
