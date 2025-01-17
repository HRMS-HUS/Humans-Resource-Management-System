from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...services import department as dept_services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from ...utils.cloudinary_helper import upload_photo
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()



@router.get("/manager/users", response_model=List[schemas.UserInfoResponse])
@limiter.limit("10/minute")
async def get_department_users(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No department found for this manager"
        )
    return await services.get_users_by_department_id(db, dept.department_id)

@router.get("/manager/users/{user_id}", response_model=schemas.UserInfoResponse)
@limiter.limit("10/minute")
async def get_user_info(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Get manager's department
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # Get user info
    user_info = await services.get_user_personal_info_by_user_id(db, user_id)
    
    # Verify user belongs to manager's department
    if user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    
    return user_info

@router.put("/manager/users/{personal_info_id}", response_model=schemas.UserInfoResponse)
@limiter.limit("5/minute")
async def update_user_info(
    request: Request,
    personal_info_id: str = Path(...),
    user_update: schemas.UserInfoUpdateNoDepartment = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Get user info first
    user_info = await services.get_user_personal_info_by_id(db, personal_info_id)
    
    # Validate manager's department
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept or user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    
    # Update user info (without changing department)
    return await services.update_user_personal_info_no_department(
        db, personal_info_id, user_update
    )

@router.put("/manager/users/{personal_info_id}/photo", response_model=schemas.UserInfoResponse)
@limiter.limit("5/minute")
async def update_user_photo(
    request: Request,
    personal_info_id: str = Path(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Get user info first
    user_info = await services.get_user_personal_info_by_id(db, personal_info_id)
    
    # Validate manager's department
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept or user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    
    # Upload and update photo
    photo_url = await upload_photo(file)
    photo_data = schemas.UserInfoPhotoUpdate(photo_url=photo_url)
    return await services.update_user_personal_info_photo(
        db, personal_info_id, photo_data
    )

@router.post("/manager/users", response_model=schemas.UserInfoResponse)
@limiter.limit("5/minute")
async def create_user_info(
    request: Request,
    user: schemas.UserInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Get manager's department
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # # Ensure user is being created in manager's department
    # if user.department_id != dept.department_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Cannot create user in different department"
    #     )
    user.department_id = dept.department_id
    return await services.create_user_info(user, db)

@router.delete("/manager/users/{personal_info_id}")
@limiter.limit("3/minute")
async def delete_user_info(
    request: Request,
    personal_info_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Get user info first to validate
    user_info = await services.get_user_personal_info_by_id(db, personal_info_id)
    
    # Validate manager's department
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept or user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    
    # Delete user info
    return await services.delete_user_personal_info(db, personal_info_id)
