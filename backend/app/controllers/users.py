from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models_user_info
from ..models import users as models
from ..schemas import users as schemas
from ..services import users as users_service
from ..utils import jwt
from fastapi import HTTPException, status, Depends, APIRouter, Query
from ..configs.database import get_db
from typing import Optional, List


router = APIRouter()


@router.get("/users/me", response_model=schemas.User)
async def read_users_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_user),
):

    return await users_service.get_user_by_id(db, current_user.user_id)


@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: str,
    user_update: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.update_user(db, user_id, user_update)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.delete_user(db, user_id)


@router.get("/users", response_model=List[schemas.User])
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
