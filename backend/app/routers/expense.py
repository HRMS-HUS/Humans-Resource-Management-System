from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import expense as admin
from ..controllers.user import expense as user
from ..controllers.manager import expense as manager
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["expense_admin"])
router.include_router(user.router, prefix="/api", tags=["expense_user"])
router.include_router(manager.router, prefix="/api", tags=["expense_manager"])
