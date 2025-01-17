from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...configs.database import get_db
from ...schemas import deptAnnouncement as schemas
from ...services import deptAnnouncement as services
from ...utils import jwt
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/admin/announcement",
    response_model=schemas.DeptAnnouncementResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("20/minute")
async def create_announcement(
    request: Request,
    announcement: schemas.DeptAnnouncementCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_dept_announcement(announcement, db)

@router.get(
    "/admin/announcement/{announcement_id}",
    response_model=schemas.DeptAnnouncementResponse
)
@limiter.limit("20/minute")
async def get_announcement(
    request: Request,
    announcement_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_dept_announcement_by_id(db, announcement_id)

@router.get(
    "/admin/announcement",
    response_model=List[schemas.DeptAnnouncementResponse]
)
@limiter.limit("20/minute")
async def get_all_announcements(
    request: Request,
    skip: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_all_dept_announcements(db, skip, limit)

@router.get(
    "/admin/announcement/department/{department_id}",
    response_model=List[schemas.DeptAnnouncementResponse]
)
@limiter.limit("20/minute")
async def get_department_announcements(
    request: Request,
    department_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_announcements_by_department_id(db, department_id)

@router.put(
    "/admin/announcement/{announcement_id}",
    response_model=schemas.DeptAnnouncementResponse
)
@limiter.limit("20/minute")
async def update_announcement(
    request: Request,
    announcement_id: str,
    announcement: schemas.DeptAnnouncementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_dept_announcement(
        db, announcement_id, announcement
    )

@router.delete("/admin/announcement/{announcement_id}")
@limiter.limit("20/minute")
async def delete_announcement(
    request: Request,
    announcement_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_dept_announcement(db, announcement_id)
