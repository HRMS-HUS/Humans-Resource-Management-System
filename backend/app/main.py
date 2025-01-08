from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import authentication, userPersonalInfo, users, userFinancialInfo, userPersonalEvent, job
from .configs.database import init_db
import os, redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(userPersonalInfo.router)
app.include_router(userFinancialInfo.router)
app.include_router(userPersonalEvent.router)
app.include_router(job.router)