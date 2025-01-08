from fastapi import FastAPI, HTTPException, APIRouter

from ..controllers.admin import users
from ..controllers.admin import userPersonalInfo as admin
from ..controllers.employee import userPersonalInfo as employee
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["personal_info_admin"])
router.include_router(employee.router, prefix="/api", tags=["personal_info_user"])