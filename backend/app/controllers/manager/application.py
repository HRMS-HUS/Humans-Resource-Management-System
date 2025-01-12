from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import application as schemas
from ...services import application as services
from ...services import userPersonalInfo as personal_info_services
from ...services import department as dept_services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

async def validate_user_in_department(db: AsyncSession, user_id: str, manager_id: str):
    # Get manager's department
    dept = await dept_services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # Get user's department
    user_info = await personal_info_services.get_user_personal_info_by_user_id(db, user_id)
    if user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    return dept

@router.post("/manager/application", response_model=schemas.ApplicationResponse)
@limiter.limit("5/minute")
async def create_application(
    request: Request,
    application: schemas.ApplicationCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, application.user_id, current_user.user_id)
    return await services.create_application(db, application)

@router.get("/manager/application/{application_id}", response_model=schemas.ApplicationResponse)
@limiter.limit("10/minute")
async def get_application(
    request: Request,
    application_id: str = Path(..., description="Application ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    application = await services.get_application_by_id(db, application_id)
    await validate_user_in_department(db, application.user_id, current_user.user_id)
    return application

@router.get("/manager/applications", response_model=List[schemas.ApplicationResponse])
@limiter.limit("10/minute")
async def get_department_applications(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    dept = await dept_services.get_department_by_manager_id(db, current_user.user_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # Get all users in department
    users = await personal_info_services.get_users_by_department_id(db, dept.department_id)
    all_applications = []
    
    # Get applications for each user
    for user in users:
        try:
            user_applications = await services.get_applications_by_user_id(db, user.user_id)
            all_applications.extend(user_applications)
        except HTTPException:
            continue
    
    return all_applications

@router.put("/manager/application/{application_id}", response_model=schemas.ApplicationResponse)
@limiter.limit("5/minute")
async def update_application(
    request: Request,
    application_id: str = Path(..., description="Application ID to update"),
    application: schemas.ApplicationUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing_app = await services.get_application_by_id(db, application_id)
    await validate_user_in_department(db, existing_app.user_id, current_user.user_id)
    return await services.update_application(db, application_id, application)

@router.delete("/manager/application/{application_id}")
@limiter.limit("3/minute")
async def delete_application(
    request: Request,
    application_id: str = Path(..., description="Application ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing_app = await services.get_application_by_id(db, application_id)
    await validate_user_in_department(db, existing_app.user_id, current_user.user_id)
    return await services.delete_application(db, application_id)
