from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...services import users as users_service
from ...schemas import userPersonalInfo as schemas
from ...services import userPersonalInfo as services
from ...database import get_db
from ...models import users as model_user


async def create_user_personal_infos(
    user: schemas.UserInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await services.create_user_info(user, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user personal info: {str(e)}",
        )


async def get_user_personal_info_by_id_controller(
    db: AsyncSession, personal_info_id: str
):
    try:
        return await services.get_user_personal_info_by_id(db, personal_info_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user personal info: {str(e)}",
        )


async def get_user_personal_info_by_user_id_controller(db: AsyncSession, user_id: str):
    try:
        return await services.get_user_personal_info_by_user_id(db, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user personal info: {str(e)}",
        )


async def update_user_personal_info_controller(
    db: AsyncSession, personal_info_id: str, user: schemas.UserInfoCreate
):
    try:
        return await services.update_user_personal_info(db, personal_info_id, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user personal info: {str(e)}",
        )


async def delete_user_personal_info_controller(db: AsyncSession, personal_info_id: str):
    try:
        return await services.delete_user_personal_info(db, personal_info_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting user personal info: {str(e)}",
        )


async def get_all_user_personal_info_controller(
    db: AsyncSession, skip: int = 0, limit: int = 100
):

    try:
        return await services.get_all_user_personal_info(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user personal info: {str(e)}",
        )
