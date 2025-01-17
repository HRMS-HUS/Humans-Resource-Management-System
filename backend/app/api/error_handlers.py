from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from ..providers.validation_exceptions import (
    UserValidationError, 
    EventValidationError, 
    FinancialValidationError,
    AuthenticationValidationError,
    PermissionValidationError
)

async def validation_exception_handler(request: Request, exc: UserValidationError):
    return JSONResponse(
        status_code=422,
        content=exc.to_dict()
    )

async def event_validation_exception_handler(request: Request, exc: EventValidationError):
    return JSONResponse(
        status_code=422,
        content=exc.to_dict()
    )

async def financial_validation_exception_handler(request: Request, exc: FinancialValidationError):
    return JSONResponse(
        status_code=422,
        content=exc.to_dict()
    )

async def auth_validation_exception_handler(request: Request, exc: AuthenticationValidationError):
    return JSONResponse(
        status_code=401,
        content=exc.to_dict()
    )

async def permission_validation_exception_handler(request: Request, exc: PermissionValidationError):
    return JSONResponse(
        status_code=403,
        content=exc.to_dict()
    )
