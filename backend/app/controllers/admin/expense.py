from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import expense as schemas
from ...models import users as models
from ...services import expense as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/admin/expense",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_expense(
    request: Request,
    expense: schemas.ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_expense(db, expense)

@router.get("/admin/expense/{expense_id}", response_model=schemas.ExpenseResponse)
@limiter.limit("10/minute")
async def get_expense_by_id(
    request: Request,
    expense_id: str = Path(..., description="Expense ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_expense_by_id(db, expense_id)

@router.put("/admin/expense/{expense_id}", response_model=schemas.ExpenseResponse)
@limiter.limit("5/minute")
async def update_expense(
    request: Request,
    expense: schemas.ExpenseUpdate,
    expense_id: str = Path(..., description="Expense ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_expense(db, expense_id, expense)

@router.delete("/admin/expense/{expense_id}")
@limiter.limit("3/minute")
async def delete_expense(
    request: Request,
    expense_id: str = Path(..., description="Expense ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_expense(db, expense_id)

@router.get("/admin/expense", response_model=List[schemas.ExpenseResponse])
@limiter.limit("10/minute")
async def get_all_expenses(
    request: Request,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_expenses(db, skip=skip, limit=limit)

@router.get("/admin/expense/user/{user_id}", response_model=List[schemas.ExpenseResponse])
@limiter.limit("10/minute")
async def get_expenses_by_user_id(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_expenses_by_user_id(db, user_id)
