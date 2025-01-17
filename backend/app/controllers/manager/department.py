from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import department as schemas
from ...services import department as services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

async def validate_manager_department(db: AsyncSession, manager_id: str, department_id: str = None):
    dept = await services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    if department_id and dept.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Not authorized for this department"
        )
    return dept

@router.get("/manager/department", response_model=schemas.DepartmentResponse)
@limiter.limit("10/minute")
async def get_own_department(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    return await services.get_department_by_manager_id(db, current_user.user_id)

@router.get("/manager/department/{department_id}", response_model=schemas.DepartmentResponse)
@limiter.limit("10/minute")
async def get_department(
    request: Request,
    department_id: str = Path(..., description="Department ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Validate access to department
    await validate_manager_department(db, current_user.user_id, department_id)
    return await services.get_department_by_id(db, department_id)

@router.put("/manager/department", response_model=schemas.DepartmentResponse)
@limiter.limit("5/minute")
async def update_own_department(
    request: Request,
    department: schemas.DepartmentUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Get manager's department
    dept = await services.get_department_by_manager_id(db, current_user.user_id)
    
    # Prevent changing critical fields
    if department.manager_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change department manager"
        )
    
    return await services.update_department(db, dept.department_id, department)
