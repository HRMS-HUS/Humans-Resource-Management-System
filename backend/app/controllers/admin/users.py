from sqlalchemy.ext.asyncio import AsyncSession
from ...models import userPersonalInfo as models_user_info
from ...models import users as models
from ...schemas import users as schemas
from ...services import users as users_service
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy import select, and_, func, text, delete
from ...utils import crypto, jwt, email, otp
from ...database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional, List


async def read_users_me(current_user: models.Users):

    return schemas.User(
        user_id=current_user.user_id, role=current_user.role, status=current_user.status
    )


async def update_existing_user(
    db: AsyncSession, user_id: str, user_update: schemas.UserCreate
):

    updated_user = await users_service.update_user(db, user_id, user_update)
    return schemas.User(
        user_id=updated_user.user_id, role=updated_user.role, status=updated_user.status
    )


async def delete_existing_user(db: AsyncSession, user_id: str):

    return await users_service.delete_user(db, user_id)


async def get_all_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    role: Optional[models.RoleEnum] = None,
    status: Optional[models.StatusEnum] = None,
) -> dict:

    users = await users_service.get_all_users(
        db, skip=skip, limit=limit, role=role, status=status
    )

    # Count total users matching filters
    total_count = await users_service.count_users(db, role=role, status=status)

    # Transform users to schema
    user_schemas = [
        schemas.User(
            user_id=user.user_id,
            username=user.username,
            role=user.role,
            status=user.status,
        )
        for user in users
    ]

    return {"users": user_schemas, "total": total_count, "skip": skip, "limit": limit}
