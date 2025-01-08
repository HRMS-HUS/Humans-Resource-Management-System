from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers import authentication, userPersonalInfo, users, userFinancialInfo, userPersonalEvent, job
from ..database import init_db
import os, redis

router = APIRouter()

router.include_router(authentication.router, prefix="/api", tags=["authentication"])