from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import department as admin
from ..controllers.user import department as user
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["department_admin"])
router.include_router(user.router, prefix="/api", tags=["department_user"])
