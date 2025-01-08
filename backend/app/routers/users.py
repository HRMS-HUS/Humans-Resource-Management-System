from fastapi import FastAPI, HTTPException, APIRouter

from ..controllers.admin import users as admin
from ..controllers.employee import users as employee
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["user_admin"])
router.include_router(employee.router, prefix="/api", tags=["user_user"])