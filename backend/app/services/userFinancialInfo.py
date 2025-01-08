# services/userFinancialInfo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import userFinancialInfo as models
from ..schemas import userFinancialInfo as schemas
from typing import List
from ..utils.redis_lock import DistributedLock

async def create_financial_info(db: AsyncSession, financial: schemas.UserFinancialInfoCreate):
    async with DistributedLock(f"financial_info:user:{financial.user_id}"):
        # Check if user already has financial info
        existing = await db.execute(
            select(models.UserFinancialInfo).filter(
                models.UserFinancialInfo.user_id == financial.user_id
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Financial info already exists for this user"
            )
            
        db_financial = models.UserFinancialInfo(
            user_id=financial.user_id,
            salaryBasic=financial.salaryBasic,
            salaryGross=financial.salaryGross,
            salaryNet=financial.salaryNet,
            allowanceHouseRent=financial.allowanceHouseRent,
            allowanceMedical=financial.allowanceMedical,
            allowanceSpecial=financial.allowanceSpecial,
            allowanceFuel=financial.allowanceFuel,
            allowancePhoneBill=financial.allowancePhoneBill,
            allowanceOther=financial.allowanceOther,
            allowanceTotal=financial.allowanceTotal,
            deductionProvidentFund=financial.deductionProvidentFund,
            deductionTax=financial.deductionTax,
            deductionOther=financial.deductionOther,
            deductionTotal=financial.deductionTotal,
            bankName=financial.bankName,
            accountName=financial.accountName,
            accountNumber=financial.accountNumber,
            iban=financial.iban
        )
        db.add(db_financial)
        await db.commit()
        await db.refresh(db_financial)
        return db_financial

async def update_financial_info(db: AsyncSession, financial_info_id: str, financial: schemas.UserFinancialInfoCreate):
    async with DistributedLock(f"financial_info:{financial_info_id}"):
        await get_financial_info_by_id(db, financial_info_id)
        
        update_data = {
            "user_id": financial.user_id,
            "salaryBasic": financial.salaryBasic,
            "salaryGross": financial.salaryGross,
            "salaryNet": financial.salaryNet,
            "allowanceHouseRent": financial.allowanceHouseRent,
            "allowanceMedical": financial.allowanceMedical,
            "allowanceSpecial": financial.allowanceSpecial,
            "allowanceFuel": financial.allowanceFuel,
            "allowancePhoneBill": financial.allowancePhoneBill,
            "allowanceOther": financial.allowanceOther,
            "allowanceTotal": financial.allowanceTotal,
            "deductionProvidentFund": financial.deductionProvidentFund,
            "deductionTax": financial.deductionTax,
            "deductionOther": financial.deductionOther,
            "deductionTotal": financial.deductionTotal,
            "bankName": financial.bankName,
            "accountName": financial.accountName,
            "accountNumber": financial.accountNumber,
            "iban": financial.iban
        }
        
        stmt = update(models.UserFinancialInfo).where(
            models.UserFinancialInfo.financial_info_id == financial_info_id
        ).values(**update_data)
        
        await db.execute(stmt)
        await db.commit()
        
        updated_info = await get_financial_info_by_id(db, financial_info_id)
        return updated_info

# The get_financial_info_by_id, get_all_financial_info, and delete_financial_info functions remain unchanged
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

async def delete_financial_info(db: AsyncSession, financial_info_id: str):
    async with DistributedLock(f"financial_info:{financial_info_id}"):
        await get_financial_info_by_id(db, financial_info_id)
        
        stmt = delete(models.UserFinancialInfo).where(
            models.UserFinancialInfo.financial_info_id == financial_info_id
        )
        
        await db.execute(stmt)
        await db.commit()
        
        return {"detail": "Financial info deleted successfully"}

async def get_user_financial_info_by_user_id(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(models.UserFinancialInfo).filter(
            models.UserFinancialInfo.user_id == user_id
        )
    )
    user_financial_info = result.scalar_one_or_none()
    
    if not user_financial_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Personal information not found for this user"
        )
    
    return user_financial_info