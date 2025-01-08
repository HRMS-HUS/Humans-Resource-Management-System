from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import users as admin
from ..controllers.user import users as user
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["user_admin"])
router.include_router(user.router, prefix="/api", tags=["user_user"])