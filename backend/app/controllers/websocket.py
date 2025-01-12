from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends, status
from ..utils import jwt
from ..configs.database import get_db
from ..services import websocket as websocket_service
from ..utils.websocket_manager import manager
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.users import Users
from ..utils.logger import logger

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Verify token first
        try:
            user_id = await jwt.decode_access_token(token)
            # Check redis token
            redis_token = await jwt.redis_client.get(user_id)
            if not redis_token:
                print("Redis token not found")
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
                
            # Get user
            current_user = await jwt.get_current_user(redis_token.decode(), db)
            
            if not current_user or current_user.status != "Active":
                print("User not active")
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
                
            print(f"User authenticated: {current_user.user_id}")
                
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Accept websocket connection
        await websocket.accept()
        
        # Add to connection manager
        manager.add_connection(current_user.user_id, websocket)
        
        try:
            while True:
                data = await websocket.receive_json()
                print(f"Received message: {data}")
                
                result = await websocket_service.handle_websocket_message(data, current_user, db)
                if result:
                    receiver_online = await manager.send_personal_message(
                        result["message"],
                        result["receiver_id"]
                    )
                    
                    await websocket_service.send_message_status(
                        result["message"]["message_id"],
                        "delivered" if receiver_online else "sent",
                        current_user.user_id
                    )

        except WebSocketDisconnect:
            print(f"WebSocket disconnected for user: {current_user.user_id}")
            manager.disconnect(current_user.user_id)
            
        except Exception as e:
            print(f"Error in websocket loop: {str(e)}")
            if not websocket.client_state.DISCONNECTED:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
            
    except Exception as e:
        print(f"Fatal connection error: {str(e)}")
        if not websocket.client_state.DISCONNECTED:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
