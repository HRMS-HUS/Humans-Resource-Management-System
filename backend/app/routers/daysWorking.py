from fastapi import APIRouter
from ..controllers.admin import daysWorking as admin_controller
from ..controllers.user import daysWorking as user_controller

router = APIRouter()

# Admin routes
router.include_router(
    admin_controller.router,
    prefix="/api",
    tags=["daysWorking_admin"]
)

# User routes
router.include_router(
    user_controller.router,
    prefix="/api",
    tags=["daysWorking_user"]
)
