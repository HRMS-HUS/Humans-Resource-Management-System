from sqlalchemy.ext.asyncio import AsyncSession
from ...models import userPersonalInfo as models_user_info
from ...models import users as models
from ...schemas import users as schemas
from ...services import users as users_service
from ...utils import jwt
from fastapi import HTTPException, status, Depends, APIRouter, Query, Path
from ...configs.database import get_db
from typing import Optional, List


router = APIRouter()


@router.put("/admin/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: str,
    user_update: schemas.UserUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.update_user(db, user_id, user_update)


@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.delete_user(db, user_id)


@router.get("/admin/users", response_model=List[schemas.User])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    role: Optional[models.RoleEnum] = Query(None, description="Filter by user role"),
    status: Optional[models.StatusEnum] = Query(
        None, description="Filter by user status"
    ),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await users_service.get_all_users(
        db, skip=skip, limit=limit, role=role, status=status
    )


@router.get("/admin/users/{user_id}", response_model=schemas.User)
async def get_user(
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.get_user_by_id(db, user_id)


# @router.put("/admin/users/{user_id}/change-password", response_model=schemas.User)
# async def admin_change_user_password(
#     user_id: str,
#     password_change: schemas.AdminChangePassword,
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(jwt.get_current_admin),
# ):
#     return await users_service.admin_change_password(
#         db,
#         user_id,
#         password_change.new_password
#     )
