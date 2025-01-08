from fastapi import FastAPI, HTTPException, APIRouter

from ..controllers.admin import users
from ..controllers import authentication
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(authentication.router, prefix="/api", tags=["authentication"])