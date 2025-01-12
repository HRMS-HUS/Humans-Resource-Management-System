from fastapi import APIRouter
from ..controllers.admin import daysWorking as admin_controller
from ..controllers.user import daysWorking as user_controller
from ..controllers.manager import daysWorking as manager_controller

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

# Manager routes
router.include_router(
    manager_controller.router,
    prefix="/api",
    tags=["daysWorking_manager"]
)
