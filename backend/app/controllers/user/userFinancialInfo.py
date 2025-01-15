# routers/userFinancialInfo.py
from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import userFinancialInfo as schemas
from ...models import users as models
from ...services import userFinancialInfo as services
from ...utils import jwt
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get("/me/financial_info", response_model=schemas.UserFinancialInfoResponse)
@limiter.limit("10/minute")
async def get_current_user_financial_info(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_financial_info_by_user_id(
        db, current_user.user_id
    )