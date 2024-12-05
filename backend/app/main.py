from fastapi import FastAPI
from .routers import authentication, userPersonalInfo, users
from .database import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(userPersonalInfo.router)