from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...configs.database import get_db
from ...schemas import department as schemas
from ...models import users as models
from ...services import department as services
from ...utils import jwt
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/admin/department",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
async def create_department(
    request: Request,
    department: schemas.DepartmentCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_department(department, db)

@router.get(
    "/admin/department/{department_id}",
    response_model=schemas.DepartmentResponse
)
@limiter.limit("10/minute")
async def get_department(
    request: Request,
    department_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_department_by_id(db, department_id)

@router.get(
    "/admin/department",
    response_model=List[schemas.DepartmentResponse]
)
@limiter.limit("10/minute")
async def get_all_departments(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_all_departments(db, skip, limit)

@router.put(
    "/admin/department/{department_id}",
    response_model=schemas.DepartmentResponse
)
@limiter.limit("5/minute")
async def update_department(
    request: Request,
    department_id: str,
    department: schemas.DepartmentUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_department(
        db, department_id, department
    )

@router.delete("/admin/department/{department_id}")
@limiter.limit("3/minute")
async def delete_department(
    request: Request,
    department_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_department(db, department_id)

@router.get(
    "/admin/department/manager/{manager_id}",
    response_model=schemas.DepartmentResponse
)
@limiter.limit("10/minute")
async def get_department_by_manager_id(
    request: Request,
    manager_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_department_by_manager_id(db, manager_id)
