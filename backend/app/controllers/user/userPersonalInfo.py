from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, File, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...services import department as dept_services
from ...models import users as models
from ...services import users
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from ...utils.cloudinary_helper import upload_photo

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get("/me/personal_info", response_model=schemas.UserInfoResponse)
@limiter.limit("10/minute")
async def get_current_user_personal_info(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_personal_info_by_user_id(
        db, current_user.user_id
    )

@router.put("/me/personal_info/{personal_info_id}", response_model=schemas.UserInfoResponse)
@limiter.limit("5/minute")
async def update_personal_info(
    request: Request,
    data: schemas.UserInfoUpdateNoDepartment = Query(...),
    personal_info_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    try:
        existing_info = await services.get_user_personal_info_by_id(db, personal_info_id)
        if existing_info.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this personal info"
            )
        
        updated_user = await services.update_user_personal_info_no_department(db, personal_info_id, data)
        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/me/personal_info/{personal_info_id}/photo", response_model=schemas.UserInfoResponse)
@limiter.limit("5/minute")
async def update_profile_photo(
    request: Request,
    file: UploadFile = File(...),
    personal_info_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    try:
        #dùng get_info theo current_user.user_id để lấy personal_info_id
        existing_info = await services.get_user_personal_info_by_id(db, personal_info_id)
        if existing_info.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this personal info"
            )
        
        photo_url = await upload_photo(file)
        photo_data = schemas.UserInfoPhotoUpdate(photo_url=photo_url)
        
        #services thêm 1 cái user_id thay vì personal_info_id
        updated_user = await services.update_user_personal_info_photo(db, personal_info_id, photo_data)
        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )