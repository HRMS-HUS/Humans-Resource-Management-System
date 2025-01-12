from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import users
from ..controllers.admin import job as admin
from ..controllers.user import job as user
from ..controllers.manager import job as manager
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["job_admin"])
router.include_router(user.router, prefix="/api", tags=["job_user"])
router.include_router(manager.router, prefix="/api", tags=["job_manager"])