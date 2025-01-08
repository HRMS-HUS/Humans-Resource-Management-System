from fastapi import FastAPI, HTTPException
from .routers import authentication, userPersonalInfo, users, userFinancialInfo, userPersonalEvent, job
from .database import init_db
import os, redis

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(userPersonalInfo.router)
app.include_router(userFinancialInfo.router)
app.include_router(userPersonalEvent.router)
app.include_router(job.router)