from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import deptAnnouncement as admin
from ..controllers.user import deptAnnouncement as user
from ..configs.database import init_db

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["announcement_admin"])
router.include_router(user.router, prefix="/api", tags=["announcement_user"])
