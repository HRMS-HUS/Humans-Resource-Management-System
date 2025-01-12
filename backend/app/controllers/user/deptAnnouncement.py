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