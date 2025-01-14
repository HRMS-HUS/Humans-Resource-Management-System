from ..providers.validation_exceptions import UserValidationError

def validate_password(password: str) -> bool:
    """Validate password length"""
    if len(password) < 6:
        raise UserValidationError("password", "Password must be at least 6 characters long")
    return True

def validate_username(username: str) -> bool:
    """Validate username length"""
    if len(username) < 4:
        raise UserValidationError("username", "Username must be at least 4 characters long")
    return True
