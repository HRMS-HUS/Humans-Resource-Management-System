from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users as models
from ..schemas import users as schemas
from fastapi import HTTPException,status
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.Users(
        username = user.username,
        password = user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
