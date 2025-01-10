from datetime import date
import re
from ..exceptions.validation_exceptions import UserValidationError

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not re.match(r'^\+?[0-9]{10,15}$', phone):
        raise UserValidationError("phone", "Invalid phone number format. Must be 10-15 digits")
    return True

def validate_citizen_card(card: str) -> bool:
    """Validate citizen card format"""
    if not re.match(r'^[0-9]{9,12}$', card):
        raise UserValidationError("citizen_card", "Citizen card must contain 9-12 digits only")
    return True

def validate_birth_date(birth_date: date) -> bool:
    """Validate employee age (18-65 years)"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise UserValidationError("date_of_birth", "Employee must be at least 18 years old")
    if age > 65:
        raise UserValidationError("date_of_birth", "Employee age exceeds retirement age")
    return True

def validate_sex(sex: str) -> bool:
    """Validate sex value"""
    valid_values = ['Male', 'Female', 'Other']
    if sex not in valid_values:
        raise UserValidationError("sex", "Sex must be one of: Male, Female, Other")
    return True

def validate_name(name: str) -> bool:
    """Validate name format"""
    if not (2 <= len(name) <= 100):
        raise UserValidationError("fullname", "Name must be between 2 and 100 characters")
    if not re.match(r'^[a-zA-Z\s\'-]+$', name):
        raise UserValidationError("fullname", "Name contains invalid characters")
    return True

def validate_address(address: str) -> bool:
    """Validate address length"""
    if not (5 <= len(address) <= 200):
        raise UserValidationError("address", "Address must be between 5 and 200 characters")
    return True

def validate_location(location: str) -> bool:
    """Validate city/country name"""
    if not (2 <= len(location) <= 100):
        raise UserValidationError("location", "Location name must be between 2 and 100 characters")
    if not re.match(r'^[a-zA-Z\s\'-]+$', location):
        raise UserValidationError("location", "Location contains invalid characters")
    return True
