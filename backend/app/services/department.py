from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, cast, Integer
from fastapi import HTTPException, status
from ..models import department as models
from ..models import userPersonalInfo as models_user_info
from ..schemas import department as schemas
from typing import List
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger
from ..services import users as user_service

class DatabaseOperationError(Exception):
    pass

async def _validate_user_exists(db: AsyncSession, user_id: str):
    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while validating user"
        )

async def create_department(
    department: schemas.DepartmentCreate, db: AsyncSession
):
    async with DistributedLock(f"department:manager:{department.manager_id}"):
        try:
            await _validate_user_exists(db, department.manager_id)
            existing = await db.execute(
                select(models.Department).filter(
                    models.Department.manager_id == department.manager_id
                )
            )
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Department already exists for this manager",
                )

            db_department = models.Department(**department.dict())
            db.add(db_department)
            await db.commit()
            await db.refresh(db_department)
            await logger.info("Created department", {
                "department_id": db_department.department_id,
                "manager_id": department.manager_id
            })
            return db_department
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception as e:
            await logger.error("Create department failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def update_department(
    db: AsyncSession, department_id: str, department: schemas.DepartmentUpdate
):
    async with DistributedLock(f"department:{department_id}"):
        try:
            db_department = await get_department_by_id(db, department_id)

            for key, value in department.dict(exclude_unset=True).items():
                setattr(db_department, key, value)

            await db.commit()
            await db.refresh(db_department)
            await logger.info("Updated department", {"department_id": department_id})
            return db_department
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception as e:
            await logger.error("Update department failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_department_by_id(db: AsyncSession, department_id: str):
    try:
        result = await db.execute(
            select(models.Department).filter(
                models.Department.department_id == department_id
            )
        )
        department = result.scalar_one_or_none()

        if not department:
            await logger.warning("Department not found", {"department_id": department_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        await logger.info("Retrieved department", {"department_id": department_id})
        return department
    except Exception as e:
        await logger.error("Get department by id failed", error=e)
        raise


async def get_all_departments(db: AsyncSession, skip: int = 0, limit: int = 200) -> List[models.Department]:
    try:
        result = await db.execute(
            select(models.Department)
            .order_by(models.Department.department_id.cast(Integer))
            .offset(skip)
            .limit(limit)
        )
        departments = result.scalars().all()
        await logger.info("Retrieved all departments", {"count": len(departments), "skip": skip, "limit": limit})
        return departments if departments else []
    except Exception as e:
        await logger.error("Get all departments failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def delete_department(db: AsyncSession, department_id: str):
    async with DistributedLock(f"department:{department_id}"):
        try:
            await get_department_by_id(db, department_id)

            stmt = delete(models.Department).where(
                models.Department.department_id == department_id
            )

            await db.execute(stmt)
            await db.commit()
            await logger.info("Deleted department", {"department_id": department_id})
            return {"detail": "Department deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception as e:
            await logger.error("Delete department failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_department_by_manager_id(db: AsyncSession, manager_id: str):
    try:
        result = await db.execute(
            select(models.Department).filter(
                models.Department.manager_id == manager_id
            )
        )
        department = result.scalar_one_or_none()

        if not department:
            await logger.warning("Department not found for manager", {"manager_id": manager_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found for this manager",
            )
        await logger.info("Retrieved department for manager", {"manager_id": manager_id})
        return department
    except Exception as e:
        await logger.error("Get department by manager failed", error=e)
        raise


async def get_user_department(db: AsyncSession, user_id: int):
    try:
        query = select(models.Department).join(
            models_user_info.UserPersonalInfo,
            models_user_info.UserPersonalInfo.department_id == models.Department.department_id
        ).where(models_user_info.UserPersonalInfo.user_id == user_id)
        
        result = await db.execute(query)
        department = result.scalar_one_or_none()
        
        if department:
            # Get manager information
            manager_info = await db.execute(
                select(models_user_info.UserPersonalInfo).filter(
                    models_user_info.UserPersonalInfo.user_id == department.manager_id
                )
            )
            manager = manager_info.scalar_one_or_none()
            
            # Create response object with manager info
            response = {
                "department_id": department.department_id,
                "name": department.department_name,
                "contact_email": department.contact_email,
                "location": department.location,
                "manager_id": department.manager_id,
                "manager": {
                    "user_id": manager.user_id,
                    "fullname": manager.fullname
                } if manager else None
            }
            
            await logger.info("Retrieved user's department", {"user_id": user_id})
            return response
        else:
            await logger.warning("No department found for user", {"user_id": user_id})
        
        return None
    except Exception as e:
        await logger.error("Get user department failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )