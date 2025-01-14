class BaseValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        return {
            "field": self.field,
            "message": self.message
        }

class UserValidationError(BaseValidationError):
    pass

class EventValidationError(BaseValidationError):
    pass

class FinancialValidationError(BaseValidationError):
    pass

class AuthenticationValidationError(BaseValidationError):
    pass

class PermissionValidationError(BaseValidationError):
    pass

