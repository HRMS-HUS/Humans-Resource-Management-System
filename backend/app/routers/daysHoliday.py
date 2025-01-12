from fastapi import APIRouter
from ..controllers.admin import daysHoliday as admin_controller
from ..controllers.user import daysHoliday as user_controller

router = APIRouter()

router.include_router(admin_controller.router, prefix="/api", tags=["Admin"])
router.include_router(user_controller.router, prefix="/api", tags=["User"])