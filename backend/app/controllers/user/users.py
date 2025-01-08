from sqlalchemy.ext.asyncio import AsyncSession
from ...models import userPersonalInfo as models_user_info
from ...models import users as models
from ...schemas import users as schemas
from ...services import users as users_service
from ...utils import jwt
from fastapi import HTTPException, status, Depends, APIRouter, Query
from ...configs.database import get_db
from typing import Optional, List


router = APIRouter()

@router.get("/me/user", response_model=schemas.User)
async def read_users_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await users_service.get_user_by_id(db, current_user.user_id)

@router.put("/me/user/change-password", response_model=schemas.User)
async def change_password(
    password_change: schemas.ChangePassword,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await users_service.change_own_password(
        db, 
        current_user,  # Pass current_user directly
        password_change.current_password,
        password_change.new_password
    )