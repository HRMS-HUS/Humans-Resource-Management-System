from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...models import users as models
from ...services import users
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from ...utils.cloudinary_helper import upload_photo

router = APIRouter()

@router.get("/me/personal_info", response_model=schemas.UserInfoResponse)
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_personal_info_by_user_id(
        db, current_user.user_id
    )

@router.put("/me/personal_info/{personal_info_id}", response_model=schemas.UserInfoResponse)
async def update_personal_info(
    data: schemas.UserInfoUpdateNoDepartment = Query(...),
    personal_info_id: str = Path(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    try:
        # Upload photo and update photo_url
        existing_info = await services.get_user_personal_info_by_id(db, personal_info_id)
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
        photo_url = await upload_photo(file)
        data.photo_url = photo_url
        
        # Call the service to update user data in DB
        updated_user = await services.update_user_personal_info_no_department(db, personal_info_id, data)

        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )