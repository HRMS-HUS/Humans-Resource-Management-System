from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import expense as schemas
from ...models import users as models
from ...services import expense as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/me/expense",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_expense_me(
    request: Request,
    expense: schemas.ExpenseCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # # Validate and set user_id
    # if expense.user_id and expense.user_id != current_user.user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot create expenses for other users"
    #     )
    expense.user_id = current_user.user_id
    return await services.create_expense(db, expense)

@router.put(
    "/me/expense/{expense_id}",
    response_model=schemas.ExpenseResponse,
)
@limiter.limit("5/minute")
async def update_expense_me(
    request: Request,
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
@limiter.limit("10/minute")
async def get_current_user_expense(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_expenses_by_user_id(
        db, current_user.user_id
    )

@router.delete("/me/expense/{expense_id}")
@limiter.limit("3/minute")
async def delete_expense_me(
    request: Request,
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
