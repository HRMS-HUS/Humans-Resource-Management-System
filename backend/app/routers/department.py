from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import department as admin
from ..controllers.user import department as user
from ..controllers.manager import department as manager
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["department_admin"])
router.include_router(user.router, prefix="/api", tags=["department_user"])
router.include_router(manager.router, prefix="/api", tags=["department_manager"])
