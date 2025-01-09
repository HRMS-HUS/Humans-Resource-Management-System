# routers/protected.py
from fastapi import APIRouter, Depends
from ..models import users as models_user
from ..utils.jwt import get_current_user, get_active_user, get_current_admin
from typing import Dict

router = APIRouter()

@router.get("/me", response_model=Dict[str, str])
async def read_me(current_user: models_user.Users = Depends(get_current_user)):
    """Test protected route that returns current user info"""
    return {
        "username": current_user.username,
        "message": "Successfully authenticated"
    }

@router.get("/admin-only")
async def admin_route(current_user: models_user.Users = Depends(get_current_admin)):
    """Test admin-only protected route"""
    return {
        "username": current_user.username,
        "message": "Admin access granted"
    }

@router.get("/active-only")
async def active_route(current_user: models_user.Users = Depends(get_active_user)):
    """Test active-user-only protected route"""
    return {
        "username": current_user.username,
        "message": "Active user access granted" 
    }