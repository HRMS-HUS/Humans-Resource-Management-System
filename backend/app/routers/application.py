from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import application as admin
from ..controllers.user import application as user
from ..controllers.manager import application as manager
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["application_admin"])
router.include_router(user.router, prefix="/api", tags=["application_user"])
router.include_router(manager.router, prefix="/api", tags=["application_manager"])
