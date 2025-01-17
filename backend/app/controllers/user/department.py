from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import department as schemas
from ...models import users as models
from ...services import department as services
from ...utils import jwt

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get("/me/department", response_model=schemas.DepartmentResponseWithManager)
@limiter.limit("20/minute")
async def get_current_user_department(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_user_department(
        db, current_user.user_id
    )