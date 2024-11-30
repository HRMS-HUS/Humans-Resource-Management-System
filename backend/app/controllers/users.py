from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import users as models
from ..schemas import users as schemas
from fastapi import HTTPException,status, Depends
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto, jwt

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.Users(
        username=user.username,
        password=user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
    try:
        username = await jwt.decode_access_token(token)
        stmt = select(models.Users).where(models.Users.username == username)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

async def get_active_user(token: str, db: AsyncSession = Depends(get_db)):
    user = await get_current_user(token, db)
    if user.status != models.StatusEnum.Active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    return user

async def get_current_admin(token: str, db: AsyncSession = Depends(get_db)):
    user = await get_active_user(token, db)
    if user.role != models.RoleEnum.Admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user