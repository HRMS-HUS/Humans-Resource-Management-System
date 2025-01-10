from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException, status
from ..models import deptAnnouncement as models
from ..schemas import deptAnnouncement as schemas
from typing import List
from ..utils.redis_lock import DistributedLock

class DatabaseOperationError(Exception):
    pass

async def create_dept_announcement(
    announcement: schemas.DeptAnnouncementCreate, 
    db: AsyncSession
):
    async with DistributedLock(f"department:announcement:{announcement.department_id}"):
        try:
            db_announcement = models.DeptAnnouncement(**announcement.dict())
            db.add(db_announcement)
            await db.commit()
            await db.refresh(db_announcement)
            return db_announcement
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

async def get_dept_announcement_by_id(db: AsyncSession, announcement_id: str):
    try:
        result = await db.execute(
            select(models.DeptAnnouncement).filter(
                models.DeptAnnouncement.announcement_id == announcement_id
            )
        )
        announcement = result.scalar_one_or_none()
        if not announcement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Announcement not found"
            )
        return announcement
    except HTTPException:
        raise

async def get_all_dept_announcements(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.DeptAnnouncement]:
    result = await db.execute(
        select(models.DeptAnnouncement).offset(skip).limit(limit)
    )
    announcements = result.scalars().all()
    return announcements if announcements else []

async def get_announcements_by_department_id(db: AsyncSession, department_id: str):
    result = await db.execute(
        select(models.DeptAnnouncement).filter(
            models.DeptAnnouncement.department_id == department_id
        )
    )
    announcements = result.scalars().all()
    return announcements if announcements else []

async def update_dept_announcement(
    db: AsyncSession, 
    announcement_id: str, 
    announcement: schemas.DeptAnnouncementUpdate
):
    async with DistributedLock(f"announcement:{announcement_id}"):
        try:
            db_announcement = await get_dept_announcement_by_id(db, announcement_id)
            
            for key, value in announcement.dict(exclude_unset=True).items():
                setattr(db_announcement, key, value)

            await db.commit()
            await db.refresh(db_announcement)
            return db_announcement
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
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

            return {"detail": "Announcement deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

