from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .routers import authentication, userPersonalInfo, users, userFinancialInfo, userPersonalEvent, job,  department, daysHoliday, daysWorking, deptAnnouncement, application, payment, userMessage, expense, websocket
from .configs.database import init_db
from .configs.cloudinary import init_cloudinary
import os, redis
from fastapi.middleware.cors import CORSMiddleware
from .providers.validation_exceptions import UserValidationError, EventValidationError, FinancialValidationError, AuthenticationValidationError, PermissionValidationError
from .api.error_handlers import validation_exception_handler, event_validation_exception_handler, financial_validation_exception_handler, auth_validation_exception_handler, permission_validation_exception_handler
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .controllers.admin.userPersonalInfo import limiter

app = FastAPI()

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def on_startup():
    await init_db()
    init_cloudinary()

# Register exception handlers
app.add_exception_handler(UserValidationError, validation_exception_handler)
app.add_exception_handler(EventValidationError, event_validation_exception_handler)
app.add_exception_handler(FinancialValidationError, financial_validation_exception_handler)
app.add_exception_handler(AuthenticationValidationError, auth_validation_exception_handler)
app.add_exception_handler(PermissionValidationError, permission_validation_exception_handler)

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(userPersonalInfo.router)
app.include_router(userFinancialInfo.router)
app.include_router(userPersonalEvent.router)
app.include_router(job.router)
app.include_router(department.router)
app.include_router(daysHoliday.router)
app.include_router(daysWorking.router)
app.include_router(deptAnnouncement.router)
app.include_router(application.router)
app.include_router(payment.router)
app.include_router(userMessage.router)
app.include_router(expense.router)
app.include_router(websocket.router)
