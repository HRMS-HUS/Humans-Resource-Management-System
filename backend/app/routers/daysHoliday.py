from fastapi import APIRouter
from ..controllers.admin import daysHoliday as admin_controller
from ..controllers.user import daysHoliday as user_controller

router = APIRouter()

# Admin routes
router.include_router(
    admin_controller.router,
    prefix="/api",
    tags=["daysHoliday_admin"]
)

# User routes
router.include_router(
    user_controller.router,
    prefix="/api",
    tags=["daysHoliday_user"]
)
