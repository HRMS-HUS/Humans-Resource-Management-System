from sqlalchemy.ext.asyncio import AsyncSession
from ...models import userPersonalInfo as models_user_info
from ...models import users as models
from ...schemas import users as schemas
from ...services import users as users_service
from ...utils import jwt
from fastapi import HTTPException, status, Depends, APIRouter, Query, Path, Request
from ...configs.database import get_db
from typing import Optional, List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.put("/admin/users/{user_id}", response_model=schemas.User)
@limiter.limit("20/minute")
async def update_user(
    request: Request,
    user_id: str,
    user_update: schemas.UserUpdate = Query(...),  # Remove Query, use as request body directly
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.update_user(db, user_id, user_update)


@router.delete("/admin/users/{user_id}")
@limiter.limit("20/minute")
async def delete_user(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.delete_user(db, user_id)


@router.get("/admin/users", response_model=List[schemas.User])
@limiter.limit("20/minute")
async def get_all_users(
    request: Request,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(200, description="Number of records to return"),
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
@limiter.limit("20/minute")
async def get_user(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await users_service.get_user_by_id(db, user_id)


