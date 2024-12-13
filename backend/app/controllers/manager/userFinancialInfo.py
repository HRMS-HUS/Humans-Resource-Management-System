# controllers/userFinancialInfo.py
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userFinancialInfo as schemas
from ...services import userFinancialInfo as services
from typing import List

async def create_financial_info_controller(
    db: AsyncSession, 
    financial: schemas.UserFinancialInfoCreate
):
    return await services.create_financial_info(db, financial)

async def get_financial_info_by_id_controller(
    db: AsyncSession, 
    financial_info_id: str
):
    return await services.get_financial_info_by_id(db, financial_info_id)

async def get_all_financial_info_controller(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[schemas.UserFinancialInfoResponse]:
    return await services.get_all_financial_info(db, skip, limit)

async def update_financial_info_controller(
    db: AsyncSession,
    financial_info_id: str,
    financial: schemas.UserFinancialInfoCreate
):
    return await services.update_financial_info(db, financial_info_id, financial)

async def delete_financial_info_controller(
    db: AsyncSession,
    financial_info_id: str
):
    return await services.delete_financial_info(db, financial_info_id)