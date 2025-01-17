from fastapi import APIRouter, Depends, HTTPException, status, Path, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...configs.database import get_db
from ...schemas import daysWorking as schemas
from ...models import users as models
from ...services import daysWorking as services
from ...utils import jwt
from typing import List
from datetime import date

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get(
    "/me/working/history",
    response_model=List[schemas.DaysWorkingResponse]
)
@limiter.limit("20/minute")
async def get_my_working_days(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    try:
        working_days = await services.get_working_day_by_user_id(
            db=db,
            user_id=current_user.user_id,
            skip=skip,
            limit=limit
        )
        if not working_days:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No working days found"
            )
        return working_days
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/me/working/{working_id}",
    response_model=schemas.DaysWorkingResponse
)
@limiter.limit("20/minute")
async def get_working_day(
    request: Request,
    working_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    working = await services.get_working_day_by_id(db, working_id)
    if working.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this working day"
        )
    return await services.get_working_day_by_id(db, working_id)
