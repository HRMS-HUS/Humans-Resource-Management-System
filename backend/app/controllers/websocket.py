from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from typing import List

connected_users: List[str] = []

router = APIRouter()
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_users.append(user_id)
    print(f"User {user_id} connected.")
    
    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message from {user_id}: {message}")
    
    except WebSocketDisconnect:
        connected_users.remove(user_id)
        print(f"User {user_id} disconnected.")


@router.get("/ws/active-users")
async def get_active_users():
    return {"active_users": connected_users}