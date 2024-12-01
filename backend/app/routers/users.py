from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models_user_info
from ..models import users as models
from ..schemas import users as schemas
from ..controllers import users
from fastapi import HTTPException,status, Depends, APIRouter, Query
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto, jwt, email, otp
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter()

@router.get("/users/get_user", response_model=schemas.UserCreate)
async def read_users_me(token: str = Query(...), db: AsyncSession = Depends(get_db), current: models.Users = Depends(users.get_current_admin)):
    user = await users.get_current_user(token, db)
    return user