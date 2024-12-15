from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import userFinancialInfo as models
from ..schemas import userFinancialInfo as schemas
from typing import List

async def create_financial_info(db: AsyncSession, financial: schemas.UserFinancialInfoCreate):
    db_financial = models.UserFinancialInfo(
        financial_info_id=financial.financial_info_id,
        user_id=financial.user_id,
        bank_name=financial.bank_name,
        account_number=financial.account_number,
        account_type=financial.account_type,
        balance=financial.balance,
        currency=financial.currency
    )
    db.add(db_financial)
    await db.commit()
    await db.refresh(db_financial)
    return db_financial

async def get_financial_info_by_id(db: AsyncSession, financial_info_id: str):
    result = await db.execute(
        select(models.UserFinancialInfo).filter(
            models.UserFinancialInfo.financial_info_id == financial_info_id
        )
    )
    financial_info = result.scalar_one_or_none()
    
    if not financial_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Financial info not found"
        )
    
    return financial_info

async def get_all_financial_info(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.UserFinancialInfo]:
    result = await db.execute(
        select(models.UserFinancialInfo)
        .offset(skip)
        .limit(limit)
    )
    financial_infos = result.scalars().all()
    
    if not financial_infos:
        return []
    
    return financial_infos

async def update_financial_info(db: AsyncSession, financial_info_id: str, financial: schemas.UserFinancialInfoCreate):
    await get_financial_info_by_id(db, financial_info_id)
    
    update_data = {
        "user_id": financial.user_id,
        "bank_name": financial.bank_name,
        "account_number": financial.account_number,
        "account_type": financial.account_type,
        "balance": financial.balance,
        "currency": financial.currency
    }
    
    stmt = update(models.UserFinancialInfo).where(
        models.UserFinancialInfo.financial_info_id == financial_info_id
    ).values(**update_data)
    
    await db.execute(stmt)
    await db.commit()
    
    updated_info = await get_financial_info_by_id(db, financial_info_id)
    return updated_info

async def delete_financial_info(db: AsyncSession, financial_info_id: str):
    await get_financial_info_by_id(db, financial_info_id)
    
    stmt = delete(models.UserFinancialInfo).where(
        models.UserFinancialInfo.financial_info_id == financial_info_id
    )
    
    await db.execute(stmt)
    await db.commit()
    
    return {"detail": "Financial info deleted successfully"}