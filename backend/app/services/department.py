from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import department as models
from ..schemas import department as schemas
from typing import List
from ..utils.redis_lock import DistributedLock


async def create_department(
    department: schemas.DepartmentCreate, db: AsyncSession
):
    async with DistributedLock(f"department:manager:{department.manager_id}"):
        # Check if manager already has a department
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
        return db_department


async def update_department(
    db: AsyncSession, department_id: str, department: schemas.DepartmentUpdate
):
    async with DistributedLock(f"department:{department_id}"):
        db_department = await get_department_by_id(db, department_id)

        for key, value in department.dict(exclude_unset=True).items():
            setattr(db_department, key, value)

        await db.commit()
        await db.refresh(db_department)
        return db_department


async def get_department_by_id(db: AsyncSession, department_id: str):
    result = await db.execute(
        select(models.Department).filter(
            models.Department.department_id == department_id
        )
    )
    department = result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )

    return department


async def get_all_departments(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Department]:
    result = await db.execute(
        select(models.Department).offset(skip).limit(limit)
    )
    departments = result.scalars().all()

    if not departments:
        return []

    return departments


async def delete_department(db: AsyncSession, department_id: str):
    async with DistributedLock(f"department:{department_id}"):
        await get_department_by_id(db, department_id)

        stmt = delete(models.Department).where(
            models.Department.department_id == department_id
        )

        await db.execute(stmt)
        await db.commit()

        return {"detail": "Department deleted successfully"}


async def get_department_by_manager_id(db: AsyncSession, manager_id: str):
    result = await db.execute(
        select(models.Department).filter(
            models.Department.manager_id == manager_id
        )
    )
    department = result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found for this manager",
        )

    return department
