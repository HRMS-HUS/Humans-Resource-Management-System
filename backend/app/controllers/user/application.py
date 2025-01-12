from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...schemas import application as schemas
from ...models import users as models
from ...services import application as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/me/application",
    response_model=schemas.ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_application_me(
    request: Request,
    application: schemas.ApplicationCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # # Validate and set user_id
    # if application.user_id and application.user_id != current_user.user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot create applications for other users"
    #     )
    application.user_id = current_user.user_id
    return await services.create_application(db, application)

@router.get(
    "/me/application",
    response_model=List[schemas.ApplicationResponse]
)
@limiter.limit("10/minute")
async def get_current_user_applications(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_applications_by_user_id(db, current_user.user_id)

@router.get(
    "/me/application/{application_id}",
    response_model=schemas.ApplicationResponse
)
@limiter.limit("10/minute")
async def get_application_me(
    request: Request,
    application_id: str = Path(..., description="Application ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    application = await services.get_application_by_id(db, application_id)
    if application.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application"
        )
    return application

@router.put(
    "/me/application/{application_id}",
    response_model=schemas.ApplicationResponse
)
@limiter.limit("5/minute")
async def update_application_me(
    request: Request,
    application_id: str = Path(..., description="Application ID to update"),
    application: schemas.ApplicationUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if application exists and belongs to current user
    existing_application = await services.get_application_by_id(db, application_id)
    if existing_application.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application"
        )
    
    # Don't allow users to update the status directly
    if application.status is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users cannot update application status"
        )
    
    return await services.update_application(db, application_id, application)

@router.delete("/me/application/{application_id}")
@limiter.limit("3/minute")
async def delete_application_me(
    request: Request,
    application_id: str = Path(..., description="Application ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if application exists and belongs to current user
    existing_application = await services.get_application_by_id(db, application_id)
    if existing_application.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this application"
        )
    
    return await services.delete_application(db, application_id)
