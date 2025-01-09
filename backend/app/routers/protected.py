from fastapi import FastAPI, HTTPException, APIRouter

from ..controllers.admin import users
from ..controllers import protected
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(protected.router, prefix="/api", tags=["protected"])