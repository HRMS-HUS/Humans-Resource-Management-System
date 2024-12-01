from fastapi import FastAPI
from .routers import userPersonalInfo, users, auth
from .database import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(userPersonalInfo.router)