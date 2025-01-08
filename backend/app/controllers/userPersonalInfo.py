from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import userPersonalInfo as schemas
from ..services import userPersonalInfo as services
from ..services import userPersonalInfo as services
from ..models import users as models
from ..services import users
from ..database import get_db
from ..utils import jwt
from typing import List

router = APIRouter()


@router.post(
    "/personal_info",
    response_model=schemas.UserInfoCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_personal_info(
    user: schemas.UserInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_user_info(db, user)


@router.get("/personal_info/{personal_info_id}", response_model=schemas.UserInfoCreate)
async def get_personal_info_by_id(
    personal_info_id: str = Path(..., description="Personal Info ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_personal_info_by_id(
        db, personal_info_id
    )


@router.get("/personal_info/user/{user_id}", response_model=schemas.UserInfoCreate)
async def get_personal_info_by_user_id(
    user_id: str = Path(..., description="User ID to retrieve personal info"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_personal_info_by_user_id(db, user_id)


@router.put("/personal_info/{personal_info_id}", response_model=schemas.UserInfoCreate)
async def update_personal_info(
    user: schemas.UserInfoCreate = Query(...),
    personal_info_id: str = Path(..., description="Personal Info ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.update_user_personal_info(
        db, personal_info_id, user
    )


@router.delete("/personal_info/{personal_info_id}")
async def delete_personal_info(
    personal_info_id: str = Path(..., description="Personal Info ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.delete_user_personal_info(db, personal_info_id)


@router.get("/personal_info", response_model=List[schemas.UserInfoCreate])
async def get_all_personal_info(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_all_user_personal_info(
        db, skip=skip, limit=limit
    )


@router.get("/me/personal_info", response_model=schemas.UserInfoCreate)
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_personal_info_by_user_id(
        db, current_user.user_id
    )
