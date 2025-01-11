from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import application as admin
from ..controllers.user import application as user
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["application_admin"])
router.include_router(user.router, prefix="/api", tags=["application_user"])
