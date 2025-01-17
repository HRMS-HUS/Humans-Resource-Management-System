from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers.admin import userMessage as admin
from ..controllers.user import userMessage as user
from ..configs.database import init_db

router = APIRouter()

router.include_router(user.router, prefix="/api", tags=["message_user"])
