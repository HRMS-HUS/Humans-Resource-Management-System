# app/routers/auth.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..configs.database import get_db
from ..schemas import users as schemas_user
from ..schemas import authentication as schemas_auth
from fastapi.security import OAuth2PasswordRequestForm
from ..services import authentication
from ..utils.jwt import get_current_user  # Add this import at the top

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

@router.post("/logout/me")
async def logout_me(
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return await authentication.logout_me(current_user, db)

@router.post("/login/admin")
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await authentication.login_admin(form_data, db)

@router.post("/verify-otp")
async def verify_otp(
    request: schemas_auth.VerifyOTP = Query(...), db: AsyncSession = Depends(get_db)
):
    return await authentication.verify_otp(request, db)

@router.post("/logout/admin")
async def logout_admin(
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return await authentication.logout_admin(current_user, db)

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

# @router.post("/logout")
# async def logout_user(
#     request: str, db: AsyncSession = Depends(get_db)
# ):
#     return await authentication.logout(request, db)

