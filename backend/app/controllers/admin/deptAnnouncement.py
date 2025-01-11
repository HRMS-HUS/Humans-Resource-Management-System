from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import deptAnnouncement as schemas
from ...services import deptAnnouncement as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.post(
    "/admin/announcement",
    response_model=schemas.DeptAnnouncementResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_announcement(
    announcement: schemas.DeptAnnouncementCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_dept_announcement(announcement, db)

@router.get(
    "/admin/announcement/{announcement_id}",
    response_model=schemas.DeptAnnouncementResponse
)
async def get_announcement(
    announcement_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_dept_announcement_by_id(db, announcement_id)

@router.get(
    "/admin/announcement",
    response_model=List[schemas.DeptAnnouncementResponse]
)
async def get_all_announcements(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_all_dept_announcements(db, skip, limit)

@router.get(
    "/admin/announcement/department/{department_id}",
    response_model=List[schemas.DeptAnnouncementResponse]
)
async def get_department_announcements(
    department_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_announcements_by_department_id(db, department_id)

@router.put(
    "/admin/announcement/{announcement_id}",
    response_model=schemas.DeptAnnouncementResponse
)
async def update_announcement(
    announcement_id: str,
    announcement: schemas.DeptAnnouncementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_dept_announcement(
        db, announcement_id, announcement
    )

@router.delete("/admin/announcement/{announcement_id}")
async def delete_announcement(
    announcement_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_dept_announcement(db, announcement_id)
