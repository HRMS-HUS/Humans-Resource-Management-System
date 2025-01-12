from fastapi import APIRouter, Depends, HTTPException, status ,Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...configs.database import get_db
from ...schemas import deptAnnouncement as schemas
from ...models import users as models
from ...services import deptAnnouncement as services
from ...services import department as dept_services
from ...utils import jwt
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# @router.get(
#     "/me/announcement", 
#     response_model=List[schemas.DeptAnnouncementResponse]
# )
# # async def get_my_department_announcements(
# #     db: AsyncSession = Depends(get_db),
# #     current_user: models.Users = Depends(jwt.get_active_user),
# # ):
# #     # Get user's department
# #     department = await dept_services.get_user_department(
# #         db, current_user.user_id
# #     )
# #     if not department:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="You don't belong to any department"
# #         )
# #     # Get announcements for that department
# #     return await services.get_announcements_by_department_id(
# #         db, department.department_id
# #     )

async def check_manager_permission(
    db: AsyncSession,
    current_user: models.Users,
    department_id: str
):
    department = await dept_services.get_department_by_id(db, department_id)
    if not department or department.manager_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to manage this department's announcements"
        )
    return department

@router.post(
    "/manager/departments/{department_id}/announcements",
    response_model=schemas.DeptAnnouncementResponse
)
@limiter.limit("5/minute")
async def create_department_announcement(
    request: Request,
    announcement: schemas.DeptAnnouncementCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    # Check if user is a manager of the department
    announcement.department_id = current_user.department_id
    await check_manager_permission(db, current_user, announcement.department_id)
    # Set department_id in announcement
    return await services.create_dept_announcement(announcement, db)

@router.put(
    "/manager/announcements/{announcement_id}",
    response_model=schemas.DeptAnnouncementResponse
)
@limiter.limit("5/minute")
async def update_department_announcement(
    request: Request,
    announcement_id: str = Path(..., description="Announcement ID to update"),
    announcement: schemas.DeptAnnouncementUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    announcement.department_id = current_user.department_id
    existing = await services.get_dept_announcement_by_id(db, announcement_id)
    await check_manager_permission(db, current_user, existing.department_id)
    return await services.update_dept_announcement(db, announcement_id, announcement)

@router.delete(
    "/manager/announcements/{announcement_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@limiter.limit("3/minute")
async def delete_department_announcement(
    request: Request,
    announcement_id: str = Path(..., description="Announcement ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    existing = await services.get_dept_announcement_by_id(db, announcement_id)
    existing.department_id = current_user.department_id
    await check_manager_permission(db, current_user, existing.department_id)
    await services.delete_dept_announcement(db, announcement_id)

@router.get(
    "/manager/departments/{department_id}/announcements",
    response_model=List[schemas.DeptAnnouncementResponse]
)
@limiter.limit("10/minute")
async def get_manager_department_announcements(
    request: Request,
    department_id: str = Path(..., description="Department ID to retrieve announcements"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    await check_manager_permission(db, current_user, department_id)
    return await services.get_announcements_by_department_id(db, department_id)

@router.get(
    "/me/announcements", 
    response_model=List[schemas.DeptAnnouncementResponse]
)
@limiter.limit("10/minute")
async def get_my_department_announcements(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    department = await dept_services.get_user_department(db, current_user.user_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't belong to any department"
        )
    return await services.get_announcements_by_department_id(db, department.department_id)