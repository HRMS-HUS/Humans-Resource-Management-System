from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import deptAnnouncement as schemas
from ...services import deptAnnouncement as services
from ...services import department as dept_services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from ...utils.logger import logger

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

async def validate_manager_department(db: AsyncSession, manager_id: str, department_id: str = None):
    dept = await dept_services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    if department_id and dept.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Not authorized for this department"
        )
    return dept

@router.post("/manager/announcement", response_model=schemas.DeptAnnouncementResponse)
@limiter.limit("5/minute")
async def create_announcement(
    request: Request,
    announcement: schemas.DeptAnnouncementCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    dept = await validate_manager_department(db, current_user.user_id)
    announcement.department_id = dept.department_id
    return await services.create_dept_announcement(announcement, db)

@router.get("/manager/announcement/{announcement_id}", response_model=schemas.DeptAnnouncementResponse)
@limiter.limit("10/minute")
async def get_announcement(
    request: Request,
    announcement_id: str = Path(..., description="Announcement ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    announcement = await services.get_dept_announcement_by_id(db, announcement_id)
    await validate_manager_department(db, current_user.user_id, announcement.department_id)
    return announcement

@router.get("/manager/announcements", response_model=List[schemas.DeptAnnouncementResponse])
@limiter.limit("10/minute")
async def get_department_announcements(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    try:
        # Get manager's department
        dept = await validate_manager_department(db, current_user.user_id)
        
        # Get announcements (will return empty list if none found)
        announcements = await services.get_announcements_by_department_id(db, dept.department_id)
        
        return announcements
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        await logger.error("Failed to get department announcements", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve announcements"
        )

@router.put("/manager/announcement/{announcement_id}", response_model=schemas.DeptAnnouncementResponse)
@limiter.limit("5/minute")
async def update_announcement(
    request: Request,
    announcement_id: str = Path(..., description="Announcement ID to update"),
    announcement: schemas.DeptAnnouncementUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing = await services.get_dept_announcement_by_id(db, announcement_id)
    await validate_manager_department(db, current_user.user_id, existing.department_id)
    
    # Ensure department can't be changed
    if announcement.department_id and announcement.department_id != existing.department_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change announcement department"
        )
    
    return await services.update_dept_announcement(db, announcement_id, announcement)

@router.delete("/manager/announcement/{announcement_id}")
@limiter.limit("3/minute")
async def delete_announcement(
    request: Request,
    announcement_id: str = Path(..., description="Announcement ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    announcement = await services.get_dept_announcement_by_id(db, announcement_id)
    await validate_manager_department(db, current_user.user_id, announcement.department_id)
    return await services.delete_dept_announcement(db, announcement_id)
