from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, File, UploadFile, Form, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...services import department as dept_services
from ...models import users as models
from ...services import users
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from ...utils.cloudinary_helper import upload_photo
import json
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post(
    "/admin/personal_info",
    response_model=schemas.UserInfoResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
async def create_user_personal_info(
    request: Request,
    user: schemas.UserInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_user_info(user, db)


@router.get("/admin/personal_info/{personal_info_id}", response_model=schemas.UserInfoResponse)
@limiter.limit("20/minute")
async def get_personal_info_by_id(
    request: Request,
    personal_info_id: str = Path(..., description="Personal Info ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_personal_info_by_id(
        db, personal_info_id
    )


@router.get("/admin/personal_info/user/{user_id}", response_model=schemas.UserInfoResponse)
@limiter.limit("20/minute")
async def get_personal_info_by_user_id(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve personal info"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_personal_info_by_user_id(db, user_id)


@router.put("/admin/personal_info/{personal_info_id}", response_model=schemas.UserInfoResponse)
@limiter.limit("20/minute")
async def update_personal_info(
    request: Request,
    data: schemas.UserInfoUpdate = Query(...),
    personal_info_id: str = Path(...),
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
        
        updated_user = await services.update_user_personal_info(db, personal_info_id, data)
        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/admin/personal_info/{personal_info_id}")
@limiter.limit("20/minute")
async def delete_personal_info(
    request: Request,
    personal_info_id: str = Path(..., description="Personal Info ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.delete_user_personal_info(db, personal_info_id)


@router.get("/admin/personal_info", response_model=List[schemas.UserInfoResponse])
@limiter.limit("20/minute")
async def get_all_personal_info(
    request: Request,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(200, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_all_user_personal_info(
        db, skip=skip, limit=limit
    )


@router.get("/admin/users/department/{department_id}", response_model=List[schemas.UserInfoResponse])
@limiter.limit("20/minute")
async def get_users_by_department(
    request: Request,
    department_id: str = Path(..., description="Department ID to get users from"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_users_by_department_id(db, department_id)

# @router.get("/manager/users/department", response_model=List[schemas.UserInfoResponse])
# @limiter.limit("10/minute")
# async def get_department_users_for_manager(
#     request: Request,
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(jwt.get_current_user),
# ):
#     # Check if user is a manager
#     dept_result = await dept_services.get_department_by_manager_id(db, current_user.user_id)
#     if not dept_result:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User is not a manager"
#         )
    
#     return await services.get_users_for_manager(db, current_user.user_id)