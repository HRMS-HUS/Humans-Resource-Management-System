from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import users as models
from ..schemas import users as schemas
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, and_, func, text, delete, update
from ..utils import crypto, jwt
from ..services import authentication
from typing import Optional, List

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.Users(
        username=user.username,
        password=user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(models.Users).filter_by(user_id=user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def update_user(db: AsyncSession, user_id: str, user_update: schemas.UserCreate):
    existing_user = await get_user_by_id(db, user_id)
    
    
    username_check = await db.execute(
        select(models.Users)
        .filter(models.Users.username == user_update.username)
        .filter(models.Users.user_id != user_id)
    )
    if username_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    
    hashed_password = crypto.hash_password(user_update.password)
    
    
    stmt = (
        update(models.Users)
        .where(models.Users.user_id == user_id)
        .values(
            username=user_update.username, 
            password=hashed_password
        )
    )
    await db.execute(stmt)
    await db.commit()
    
    
    await db.refresh(existing_user)
    return existing_user

async def delete_user(db: AsyncSession, user_id: str):
    await get_user_by_id(db, user_id)
    
    
    stmt = delete(models.Users).where(models.Users.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    
    return {"detail": "User deleted successfully"}

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(jwt.oauth2_scheme)):
    return await jwt.get_current_user(token, db)

async def get_active_user(db: AsyncSession = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    if current_user.status != models.StatusEnum.Active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    return current_user

async def get_current_admin(db: AsyncSession = Depends(get_db), current_user: models.Users = Depends(get_active_user)):
    if current_user.role != models.RoleEnum.Admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

async def get_all_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10, 
    role: Optional[models.RoleEnum] = None, 
    status: Optional[models.StatusEnum] = None
) -> List[models.Users]:
    query = select(models.Users)
    
    
    if role is not None:
        query = query.filter(models.Users.role == role)
    
    
    if status is not None:
        query = query.filter(models.Users.status == status)
    
    
    query = query.offset(skip).limit(limit)
    
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users

async def count_users(
    db: AsyncSession, 
    role: Optional[models.RoleEnum] = None, 
    status: Optional[models.StatusEnum] = None
) -> int:
    
    query = select(func.count(models.Users.user_id))
    
    
    if role is not None:
        query = query.filter(models.Users.role == role)
    
    
    if status is not None:
        query = query.filter(models.Users.status == status)
    
    
    result = await db.execute(query)
    return result.scalar_one()