from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import expense as schemas
from ...models import users as models
from ...services import expense as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/admin/expense",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense(
    expense: schemas.ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_expense(db, expense)

@router.get("/admin/expense/{expense_id}", response_model=schemas.ExpenseResponse)
async def get_expense_by_id(
    expense_id: str = Path(..., description="Expense ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_expense_by_id(db, expense_id)

@router.put("/admin/expense/{expense_id}", response_model=schemas.ExpenseResponse)
async def update_expense(
    expense: schemas.ExpenseUpdate,
    expense_id: str = Path(..., description="Expense ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_expense(db, expense_id, expense)

@router.delete("/admin/expense/{expense_id}")
async def delete_expense(
    expense_id: str = Path(..., description="Expense ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_expense(db, expense_id)

@router.get("/admin/expense", response_model=List[schemas.ExpenseResponse])
async def get_all_expenses(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_expenses(db, skip=skip, limit=limit)

@router.get("/admin/expense/user/{user_id}", response_model=List[schemas.ExpenseResponse])
async def get_expenses_by_user_id(
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_expenses_by_user_id(db, user_id)
