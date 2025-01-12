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
    "/admin/application",
    response_model=schemas.ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_application(
    request: Request,
    application: schemas.ApplicationCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_application(db, application)

@router.get(
    "/admin/application/{application_id}",
    response_model=schemas.ApplicationResponse
)
@limiter.limit("10/minute")
async def get_application_by_id(
    request: Request,
    application_id: str = Path(..., description="Application ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_application_by_id(db, application_id)

@router.put(
    "/admin/application/{application_id}",
    response_model=schemas.ApplicationResponse
)
@limiter.limit("5/minute")
async def update_application(
    request: Request,
    application: schemas.ApplicationUpdate = Query(...),
    application_id: str = Path(..., description="Application ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_application(db, application_id, application)

@router.delete("/admin/application/{application_id}")
@limiter.limit("3/minute")
async def delete_application(
    request: Request,
    application_id: str = Path(..., description="Application ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_application(db, application_id)

@router.get(
    "/admin/application",
    response_model=List[schemas.ApplicationResponse]
)
@limiter.limit("10/minute")
async def get_all_applications(
    request: Request,
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
@limiter.limit("10/minute")
async def get_applications_by_user_id(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_applications_by_user_id(db, user_id)
