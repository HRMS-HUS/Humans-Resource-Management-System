from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import daysWorking as schemas
from ...services import daysWorking as services
from ...services import department as dept_services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import date

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

async def validate_manager_role(db: AsyncSession, manager_id: str):
    dept = await dept_services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    return dept

@router.post("/manager/working", response_model=schemas.DaysWorkingResponse)
@limiter.limit("5/minute")
async def create_working_day(
    request: Request,
    working: schemas.DaysWorkingCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Verify manager has a department
    await validate_manager_role(db, current_user.user_id)
    return await services.create_working_day(working, db)

@router.get("/manager/working/{working_id}", response_model=schemas.DaysWorkingResponse)
@limiter.limit("10/minute")
async def get_working_day(
    request: Request,
    working_id: str = Path(..., description="Working ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Verify manager has a department
    await validate_manager_role(db, current_user.user_id)
    return await services.get_working_day_by_id(db, working_id)

@router.get("/manager/working", response_model=List[schemas.DaysWorkingResponse])
@limiter.limit("10/minute")
async def get_all_working_days(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Verify manager has a department
    await validate_manager_role(db, current_user.user_id)
    return await services.get_all_working_days(db, skip, limit)

@router.put("/manager/working/{working_id}", response_model=schemas.DaysWorkingResponse)
@limiter.limit("5/minute")
async def update_working_day(
    request: Request,
    working_id: str = Path(..., description="Working ID to update"),
    working: schemas.DaysWorkingUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Verify manager has a department
    await validate_manager_role(db, current_user.user_id)
    return await services.update_working_day(db, working_id, working)

@router.delete("/manager/working/{working_id}")
@limiter.limit("3/minute")
async def delete_working_day(
    request: Request,
    working_id: str = Path(..., description="Working ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Verify manager has a department
    await validate_manager_role(db, current_user.user_id)
    return await services.delete_working_day(db, working_id)

@router.get("/manager/working/user/{user_id}", response_model=List[schemas.DaysWorkingResponse])
@limiter.limit("10/minute")
async def get_user_working_days(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve working days"),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Verify manager has a department
    dept = await validate_manager_role(db, current_user.user_id)
    
    # Add validation to ensure user belongs to manager's department
    user_dept = await dept_services.get_user_department(db, user_id)
    if not user_dept or user_dept.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to your department"
        )
    
    return await services.get_working_day_by_user_id(db, user_id, skip, limit)

# @router.get("/manager/attendance", response_model=List[schemas.DaysWorkingResponse])
# @limiter.limit("10/minute")
# async def get_department_attendance(
#     request: Request,
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(jwt.get_current_manager)
# ):
#     await validate_manager_role(db, current_user.user_id)
#     return await services.get_all_working_days(db, skip, limit)

# @router.get("/manager/attendance/{working_id}", response_model=schemas.DaysWorkingResponse)
# @limiter.limit("10/minute")
# async def get_attendance_record(
#     request: Request,
#     working_id: str = Path(...),
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(jwt.get_current_manager)
# ):
#     await validate_manager_role(db, current_user.user_id)
#     return await services.get_working_day_by_id(db, working_id)

# @router.put("/manager/attendance/{working_id}", response_model=schemas.DaysWorkingResponse)
# @limiter.limit("5/minute")
# async def update_attendance_record(
#     request: Request,
#     working_id: str = Path(...),
#     working: schemas.DaysWorkingUpdate = Query(...),
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(jwt.get_current_manager)
# ):
#     await validate_manager_role(db, current_user.user_id)
#     return await services.update_working_day(db, working_id, working)
