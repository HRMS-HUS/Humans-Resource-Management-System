from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException, status
from ..models import deptAnnouncement as models
from ..models import department as models_department  # Add this import
from ..schemas import deptAnnouncement as schemas
from typing import List
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger

class DatabaseOperationError(Exception):
    pass

async def _validate_department_exists(db: AsyncSession, department_id: str):
    try:
        if department_id:
            result = await db.execute(
                select(models_department.Department).filter(
                    models_department.Department.department_id == department_id
                )
            )
            department = result.scalar_one_or_none()
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Department not found"
                )
            return department
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while validating department"
        )

async def create_dept_announcement(
    announcement: schemas.DeptAnnouncementCreate, 
    db: AsyncSession
):
    async with DistributedLock(f"department:announcement:{announcement.department_id}"):
        try:
            # Validate department exists
            await _validate_department_exists(db, announcement.department_id)
            
            db_announcement = models.DeptAnnouncement(**announcement.dict())
            db.add(db_announcement)
            await db.commit()
            await db.refresh(db_announcement)
            await logger.info("Created department announcement", {
                "announcement_id": db_announcement.announcement_id,
                "department_id": announcement.department_id
            })
            return db_announcement
        except Exception as e:
            await logger.error("Create department announcement failed", error=e)
            await db.rollback()
            raise

async def get_dept_announcement_by_id(db: AsyncSession, announcement_id: str):
    try:
        result = await db.execute(
            select(models.DeptAnnouncement).filter(
                models.DeptAnnouncement.announcement_id == announcement_id
            )
        )
        announcement = result.scalar_one_or_none()
        if not announcement:
            await logger.warning("Announcement not found", {"announcement_id": announcement_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Announcement not found"
            )
        await logger.info("Retrieved announcement", {"announcement_id": announcement_id})
        return announcement
    except Exception as e:
        await logger.error("Get announcement by id failed", error=e)
        raise

async def get_all_dept_announcements(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.DeptAnnouncement]:
    try:
        result = await db.execute(
            select(models.DeptAnnouncement).offset(skip).limit(limit)
        )
        announcements = result.scalars().all()
        await logger.info("Retrieved all announcements", {"count": len(announcements), "skip": skip, "limit": limit})
        return announcements if announcements else []
    except Exception as e:
        await logger.error("Get all announcements failed", error=e)
        raise

async def get_announcements_by_department_id(db: AsyncSession, department_id: str):
    try:
        result = await db.execute(
            select(models.DeptAnnouncement)
            .filter(models.DeptAnnouncement.department_id == department_id)
        )
        announcements = result.scalars().all()
        
        # Log the result but don't raise exception
        if not announcements:
            await logger.info("No announcements found for department", {"department_id": department_id})
            return []
            
        await logger.info(
            "Retrieved announcements for department", 
            {"department_id": department_id, "count": len(announcements)}
        )
        return announcements

    except Exception as e:
        await logger.error("Get department announcements failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving announcements"
        )

async def update_dept_announcement(
    db: AsyncSession, 
    announcement_id: str, 
    announcement: schemas.DeptAnnouncementUpdate
):
    async with DistributedLock(f"announcement:{announcement_id}"):
        try:
            db_announcement = await get_dept_announcement_by_id(db, announcement_id)
            
            # Validate department if it's being updated
            if announcement.department_id:
                await _validate_department_exists(db, announcement.department_id)
                
            # Changed to use exclude_unset=True
            update_data = announcement.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_announcement, key, value)

            await db.commit()
            await db.refresh(db_announcement)
            await logger.info("Updated department announcement", {
                "announcement_id": db_announcement.announcement_id,
                "department_id": db_announcement.department_id
            })
            return db_announcement
        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await logger.error("Update department announcement failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def delete_dept_announcement(db: AsyncSession, announcement_id: str):
    async with DistributedLock(f"announcement:{announcement_id}"):
        try:
            await get_dept_announcement_by_id(db, announcement_id)

            stmt = delete(models.DeptAnnouncement).where(
                models.DeptAnnouncement.announcement_id == announcement_id
            )
            await db.execute(stmt)
            await db.commit()
            await logger.info("Deleted department announcement", {
                "announcement_id": announcement_id
            })
            return {"detail": "Announcement deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await logger.error("Delete department announcement failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

