from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import userPersonalInfo as schemas
from ..controllers.manager import userPersonalInfo as controllers
from ..models import users as models
from ..services import users
from ..database import get_db
from typing import List

router = APIRouter(prefix="/api", tags=["personal_info"])


@router.post(
    "/personal_info",
    response_model=schemas.UserInfoCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_personal_info(
    user: schemas.UserInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.create_user_personal_infos(db, user)


@router.get("/personal_info/{personal_info_id}", response_model=schemas.UserInfoCreate)
async def get_personal_info_by_id(
    personal_info_id: str = Path(..., description="Personal Info ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):

    return await controllers.get_user_personal_info_by_id_controller(
        db, personal_info_id
    )


@router.get("/personal_info/user/{user_id}", response_model=schemas.UserInfoCreate)
async def get_personal_info_by_user_id(
    user_id: str = Path(..., description="User ID to retrieve personal info"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):

    return await controllers.get_user_personal_info_by_user_id_controller(db, user_id)


@router.put("/personal_info/{personal_info_id}", response_model=schemas.UserInfoCreate)
async def update_personal_info(
    user: schemas.UserInfoCreate = Query(...),
    personal_info_id: str = Path(..., description="Personal Info ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):

    return await controllers.update_user_personal_info_controller(
        db, personal_info_id, user
    )


@router.delete("/personal_info/{personal_info_id}")
async def delete_personal_info(
    personal_info_id: str = Path(..., description="Personal Info ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):

    return await controllers.delete_user_personal_info_controller(db, personal_info_id)


@router.get("/personal_info", response_model=List[schemas.UserInfoCreate])
async def get_all_personal_info(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):

    return await controllers.get_all_user_personal_info_controller(
        db, skip=skip, limit=limit
    )


@router.get("/me/personal_info", response_model=schemas.UserInfoCreate)
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_user),
):

    return await controllers.get_user_personal_info_by_user_id_controller(
        db, current_user.user_id
    )
