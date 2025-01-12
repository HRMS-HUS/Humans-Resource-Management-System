from sqlalchemy.ext.asyncio import AsyncSession
from ..models import expense as models
from ..schemas import expense as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger
from ..services import users as user_service

async def _validate_user_exists(db: AsyncSession, user_id: str):
    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while validating user"
        )

async def create_expense(db: AsyncSession, expense: schemas.ExpenseCreate):
    async with DistributedLock(f"expense:user:{expense.user_id}"):
        try:
            await _validate_user_exists(db, expense.user_id)
            db_expense = models.Expense(
                user_id=expense.user_id,
                expense_item_name=expense.expense_item_name,
                expense_item_store=expense.expense_item_store,
                expense_date=expense.expense_date,
                amount=expense.amount
            )
            db.add(db_expense)
            await db.commit()
            await db.refresh(db_expense)
            await logger.info("Created expense", {
                "expense_id": db_expense.expense_id,
                "user_id": expense.user_id
            })
            return db_expense
        except Exception as e:
            await logger.error("Create expense failed", error=e)
            await db.rollback()
            raise

async def get_expense_by_id(db: AsyncSession, expense_id: str):
    try:
        result = await db.execute(
            select(models.Expense).filter(
                models.Expense.expense_id == expense_id
            )
        )
        expense = result.scalar_one_or_none()

        if not expense:
            await logger.warning("Expense not found", {"expense_id": expense_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        await logger.info("Retrieved expense by id", {"expense_id": expense_id})
        return expense
    except Exception as e:
        await logger.error("Get expense by id failed", error=e)
        raise

async def get_expenses_by_user_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.Expense).filter(
                models.Expense.user_id == user_id
            )
        )
        expenses = result.scalars().all()
        await logger.info("Retrieved expenses for user", {"user_id": user_id, "count": len(expenses)})
        return expenses
    except Exception as e:
        await logger.error("Get expenses by user failed", error=e)
        raise

async def get_all_expenses(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Expense]:
    try:
        result = await db.execute(
            select(models.Expense).offset(skip).limit(limit)
        )
        expenses = result.scalars().all()
        await logger.info("Retrieved all expenses", {"count": len(expenses), "skip": skip, "limit": limit})
        return expenses
    except Exception as e:
        await logger.error("Get all expenses failed", error=e)
        raise

async def update_expense(
    db: AsyncSession, expense_id: str, expense: schemas.ExpenseUpdate
):
    async with DistributedLock(f"expense:{expense_id}"):
        try:
            query = (
                update(models.Expense)
                .where(models.Expense.expense_id == expense_id)
                .values(expense.dict(exclude_unset=True))
            )

            result = await db.execute(query)
            await db.commit()

            if result.rowcount == 0:
                await logger.warning("Expense not found for update", {"expense_id": expense_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
                )

            await logger.info("Updated expense", {"expense_id": expense_id})
            return await get_expense_by_id(db, expense_id)
        except Exception as e:
            await logger.error("Update expense failed", error=e)
            await db.rollback()
            raise

async def delete_expense(db: AsyncSession, expense_id: str):
    async with DistributedLock(f"expense:{expense_id}"):
        try:
            result = await db.execute(
                delete(models.Expense).where(
                    models.Expense.expense_id == expense_id
                )
            )
            await db.commit()

            if result.rowcount == 0:
                await logger.warning("Expense not found for deletion", {"expense_id": expense_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
                )

            await logger.info("Deleted expense", {"expense_id": expense_id})
            return {"message": "Expense deleted successfully"}
        except Exception as e:
            await logger.error("Delete expense failed", error=e)
            await db.rollback()
            raise
