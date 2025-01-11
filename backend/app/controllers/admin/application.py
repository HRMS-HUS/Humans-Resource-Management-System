from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import application as schemas
from ...models import users as models
from ...services import application as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/admin/application",
    response_model=schemas.ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    application: schemas.ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_application(db, application)

@router.get(
    "/admin/application/{application_id}",
    response_model=schemas.ApplicationResponse
)
async def get_application_by_id(
    application_id: str = Path(..., description="Application ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_application_by_id(db, application_id)

@router.put(
    "/admin/application/{application_id}",
    response_model=schemas.ApplicationResponse
)
async def update_application(
    application: schemas.ApplicationUpdate,
    application_id: str = Path(..., description="Application ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_application(db, application_id, application)

@router.delete("/admin/application/{application_id}")
async def delete_application(
    application_id: str = Path(..., description="Application ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_application(db, application_id)

@router.get(
    "/admin/application",
    response_model=List[schemas.ApplicationResponse]
)
async def get_all_applications(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_applications(db, skip=skip, limit=limit)

@router.get(
    "/admin/application/user/{user_id}",
    response_model=List[schemas.ApplicationResponse]
)
async def get_applications_by_user_id(
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_applications_by_user_id(db, user_id)
