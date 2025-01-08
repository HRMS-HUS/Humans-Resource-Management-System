from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers import authentication, userPersonalInfo, users, userFinancialInfo, userPersonalEvent, job
from ..configs.database import init_db
import os, redis

router = APIRouter()

router.include_router(userPersonalEvent.router, prefix="/api", tags=["personal_event"])