from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, File, UploadFile, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...services import userPersonalInfo as services
from ...models import users as models
from ...services import users
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from ...utils.cloudinary_helper import upload_photo
import json

router = APIRouter()


@router.post(
    "/admin/personal_info",
    response_model=schemas.UserInfoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_personal_info(
    user: schemas.UserInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_user_info(user, db)


@router.get("/admin/personal_info/{personal_info_id}", response_model=schemas.UserInfoResponse)
async def get_personal_info_by_id(
    personal_info_id: str = Path(..., description="Personal Info ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_personal_info_by_id(
        db, personal_info_id
    )


@router.get("/admin/personal_info/user/{user_id}", response_model=schemas.UserInfoResponse)
async def get_personal_info_by_user_id(
    user_id: str = Path(..., description="User ID to retrieve personal info"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_personal_info_by_user_id(db, user_id)


@router.put("/admin/personal_info/{personal_info_id}", response_model=schemas.UserInfoResponse)
async def update_personal_info(
    data: schemas.UserInfoUpdate = Query(...),
    personal_info_id: str = Path(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    try:
        existing_info = await services.get_user_personal_info_by_id(db, personal_info_id)
        if not existing_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal info not found"
            )
        # Upload photo and update photo_url
        photo_url = await upload_photo(file)
        data.photo_url = photo_url
        
        # Call the service to update user data in DB
        updated_user = await services.update_user_personal_info(db, personal_info_id, data)

        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# @router.put("/admin/personal_info/{personal_info_id}/photo", response_model=schemas.UserInfoResponse)
# async def update_user_photo(
#     personal_info_id: str,
#     users: schemas.UserInfoUpdate,
    
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(jwt.get_current_admin),
# ):
#     # Upload photo and get URL
#     photo_url = await upload_photo(file)
    
#     # Update the personal info with the new photo URL
#     return await services.update_user_personal_info(db, personal_info_id, users)


@router.delete("/admin/personal_info/{personal_info_id}")
async def delete_personal_info(
    personal_info_id: str = Path(..., description="Personal Info ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.delete_user_personal_info(db, personal_info_id)


@router.get("/admin/personal_info", response_model=List[schemas.UserInfoResponse])
async def get_all_personal_info(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_all_user_personal_info(
        db, skip=skip, limit=limit
    )
