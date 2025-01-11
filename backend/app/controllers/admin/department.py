from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import department as schemas
from ...models import users as models
from ...services import department as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.post(
    "/admin/department",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_department(
    department: schemas.DepartmentCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_department(department, db)

@router.get(
    "/admin/department/{department_id}",
    response_model=schemas.DepartmentResponse
)
async def get_department(
    department_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_department_by_id(db, department_id)

@router.get(
    "/admin/department",
    response_model=List[schemas.DepartmentResponse]
)
async def get_all_departments(
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
async def update_department(
    department_id: str,
    department: schemas.DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_department(
        db, department_id, department
    )

@router.delete("/admin/department/{department_id}")
async def delete_department(
    department_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_department(db, department_id)

@router.get(
    "/admin/department/manager/{manager_id}",
    response_model=schemas.DepartmentResponse
)
async def get_department_by_manager_id(
    manager_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_department_by_manager_id(db, manager_id)
