# services/userFinancialInfo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException
from ..models import userFinancialInfo as models
from ..schemas import userFinancialInfo as schemas
from typing import List

async def create_financial_info(db: AsyncSession, financial: schemas.UserFinancialInfoCreate):
    db_financial = models.UserFinancialInfo(
        **financial.model_dump()
    )
    db.add(db_financial)
    await db.commit()
    await db.refresh(db_financial)
    return db_financial

async def get_financial_info_by_id(db: AsyncSession, financial_info_id: str):
    result = await db.execute(
        select(models.UserFinancialInfo)
        .filter(models.UserFinancialInfo.financial_info_id == financial_info_id)
    )
    if not (financial := result.scalar_one_or_none()):
        raise HTTPException(status_code=404, detail="Financial info not found")
    return financial

async def get_all_financial_info(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.UserFinancialInfo]:
    result = await db.execute(
        select(models.UserFinancialInfo)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_financial_info(db: AsyncSession, financial_info_id: str, financial: schemas.UserFinancialInfoCreate):
    await get_financial_info_by_id(db, financial_info_id)
    stmt = update(models.UserFinancialInfo).where(
        models.UserFinancialInfo.financial_info_id == financial_info_id
    ).values(**financial.model_dump())
    await db.execute(stmt)
    await db.commit()
    return await get_financial_info_by_id(db, financial_info_id)

async def delete_financial_info(db: AsyncSession, financial_info_id: str):
    await get_financial_info_by_id(db, financial_info_id)
    stmt = delete(models.UserFinancialInfo).where(
        models.UserFinancialInfo.financial_info_id == financial_info_id
    )
    await db.execute(stmt)
    await db.commit()
    return {"detail": "Financial info deleted successfully"}