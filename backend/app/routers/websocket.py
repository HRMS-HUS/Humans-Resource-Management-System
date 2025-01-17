from fastapi import FastAPI, HTTPException, APIRouter
from ..controllers import websocket

router = APIRouter()

router.include_router(websocket.router, prefix="/api", tags=["websocket"])