from datetime import date
import re
from ..providers.validation_exceptions import UserValidationError

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if phone is None:
        raise UserValidationError("phone", "Phone number is required")
    if not re.match(r'^\+?[0-9]{10,15}$', phone):
        raise UserValidationError("phone", "Invalid phone number format. Must be 10-15 digits")
    return True

def validate_citizen_card(card: str) -> bool:
    """Validate citizen card format"""
    if card is None:
        raise UserValidationError("citizen_card", "Citizen card is required")
    if not re.match(r'^[0-9]{9,12}$', card):
        raise UserValidationError("citizen_card", "Citizen card must contain 9-12 digits only")
    return True
