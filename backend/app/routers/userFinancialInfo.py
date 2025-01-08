from fastapi import FastAPI, HTTPException, APIRouter

from ..controllers.admin import users
from ..controllers.admin import userFinancialInfo as admin
from ..controllers.employee import userFinancialInfo as employee
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["financial_info_admin"])
router.include_router(employee.router, prefix="/api", tags=["financial_info_user"])