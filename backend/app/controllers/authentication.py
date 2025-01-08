# app/routers/auth.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import users as schemas_user
from ..schemas import authentication as schemas_auth
from fastapi.security import OAuth2PasswordRequestForm
from ..services import authentication

router = APIRouter()


@router.post("/register")
async def register_user(
    user: schemas_user.UserCreate = Query(...), db: AsyncSession = Depends(get_db)
):
    return await authentication.register(user, db)


@router.post("/login")
async def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await authentication.login(form_data, db)


@router.post("/forgot-password")
async def forgot_password_request(
    request: schemas_auth.ForgotPassword = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await authentication.forgot_password(request, db)


@router.post("/reset-password")
async def reset_password(
    request: schemas_auth.ResetPassword = Query(...), db: AsyncSession = Depends(get_db)
):
    return await authentication.reset_passwords(request, db)
