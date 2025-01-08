from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import users
from ..controllers.admin import userPersonalInfo as admin
from ..controllers.user import userPersonalInfo as user
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["personal_info_admin"])
router.include_router(user.router, prefix="/api", tags=["personal_info_user"])