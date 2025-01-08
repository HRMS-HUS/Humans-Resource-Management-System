from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import users
from ..controllers.admin import userPersonalEvent as admin
from ..controllers.user import userPersonalEvent as user
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(admin.router, prefix="/api", tags=["personal_event_admin"])
router.include_router(user.router, prefix="/api", tags=["personal_event_user"])