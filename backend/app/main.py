from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import authentication, userPersonalInfo, users, userFinancialInfo, userPersonalEvent, job,  department, daysHoliday, daysWorking
from .configs.database import init_db
import os, redis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# origins = [
#    "http://192.168.211.:8000",
#    "http://localhost",
#    "http://localhost:8080",
# ]
# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
# )

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(userPersonalInfo.router)
app.include_router(userFinancialInfo.router)
app.include_router(userPersonalEvent.router)
app.include_router(job.router)
app.include_router(department.router)
app.include_router(daysHoliday.router)
app.include_router(daysWorking.router)