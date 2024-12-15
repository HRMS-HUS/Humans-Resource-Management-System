from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import users as users_service
from ..schemas import userPersonalEvent as schemas
from ..services import userPersonalEvent as services
from ..database import get_db
from ..models import users as model_user

async def create_user_event(
    db: AsyncSession,
    event: schemas.UserPersonalEventCreate,
):
    try:
        return await services.create_user_event(db, event)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user event: {str(e)}",
        )

async def get_user_event_by_id_controller(
    db: AsyncSession, event_id: str
):
    try:
        return await services.get_user_event_by_id(db, event_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user event: {str(e)}",
        )

async def get_user_events_by_user_id_controller(db: AsyncSession, user_id: str):
    try:
        return await services.get_user_event_by_user_id(db, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user events: {str(e)}",
        )

async def update_user_event_controller(
    db: AsyncSession, event_id: str, event: schemas.UserPersonalEventUpdate
):
    try:
        return await services.update_user_event(db, event_id, event)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user event: {str(e)}",
        )

async def delete_user_event_controller(db: AsyncSession, event_id: str):
    try:
        return await services.delete_user_event(db, event_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting user event: {str(e)}",
        )

async def get_all_user_events_controller(
    db: AsyncSession, skip: int = 0, limit: int = 100
):
    try:
        result = await services.get_all_events(db, skip=skip, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user events: {str(e)}",
        )