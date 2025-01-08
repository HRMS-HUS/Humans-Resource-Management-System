from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...models import users as models
from ...services import users
from ...configs.database import get_db
from ...utils import jwt
from typing import List

router = APIRouter()

@router.get("/me/personal_info", response_model=schemas.UserInfoResponse)
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_personal_info_by_user_id(
        db, current_user.user_id
    )

@router.put(
    "/me/personal_info/{personal_id}",
    response_model=schemas.UserInfoResponse,
)
async def update_current_user_personal_info(
    personal_id: str,
    info_update: schemas.UserInfoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if personal info exists and belongs to current user
    existing_info = await services.get_user_personal_info_by_id(db, personal_id)
    if not existing_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal info not found"
        )
    if existing_info.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this personal info"
        )
    
    return await services.update_user_personal_info(db, personal_id, info_update)
