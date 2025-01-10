from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from ..exceptions.validation_exceptions import UserValidationError, EventValidationError, FinancialValidationError

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

