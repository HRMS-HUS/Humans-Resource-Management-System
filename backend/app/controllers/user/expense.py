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
    "/me/expense",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense_me(
    expense: schemas.ExpenseCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Validate and set user_id
    if expense.user_id and expense.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create expenses for other users"
        )
    expense.user_id = current_user.user_id
    return await services.create_expense(db, expense)

@router.put(
    "/me/expense/{expense_id}",
    response_model=schemas.ExpenseResponse,
)
async def update_expense_me(
    expense_id: str = Path(..., description="Expense ID to update"),
    expense_update: schemas.ExpenseUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if expense exists and belongs to current user
    existing_expense = await services.get_expense_by_id(db, expense_id)
    if not existing_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    if existing_expense.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this expense"
        )
    
    return await services.update_expense(db, expense_id, expense_update)

@router.get("/me/expense", response_model=List[schemas.ExpenseResponse])
async def get_current_user_expense(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_expenses_by_user_id(
        db, current_user.user_id
    )

@router.delete("/me/expense/{expense_id}")
async def delete_expense_me(
    expense_id: str = Path(..., description="Expense ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if expense exists and belongs to current user
    expense = await services.get_expense_by_id(db, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    if expense.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this expense"
        )
    
    return await services.delete_expense(db, expense_id)
