from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import payment as admin
from ..controllers.user import payment as user
from ..controllers.manager import payment as manager
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["payment_admin"])
router.include_router(user.router, prefix="/api", tags=["payment_user"])
router.include_router(manager.router, prefix="/api", tags=["payment_manager"])
