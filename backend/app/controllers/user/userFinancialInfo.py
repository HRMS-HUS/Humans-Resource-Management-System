# routers/userFinancialInfo.py
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import userFinancialInfo as schemas
from ...models import users as models
from ...services import userFinancialInfo as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.get("/me/financial_info", response_model=schemas.UserFinancialInfoResponse)
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_financial_info_by_user_id(
        db, current_user.user_id
    )