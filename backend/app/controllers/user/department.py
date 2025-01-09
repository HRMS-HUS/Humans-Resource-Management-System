from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import department as schemas
from ...models import users as models
from ...services import department as services
from ...utils import jwt

router = APIRouter()

@router.get("/me/department", response_model=schemas.DepartmentResponse)
async def get_current_user_department(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_department_by_manager_id(
        db, current_user.user_id
    )
