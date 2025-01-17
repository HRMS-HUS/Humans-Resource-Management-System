from datetime import date
from ..providers.validation_exceptions import EventValidationError


def validate_event_dates(start_date: date, end_date: date) -> bool:
    """Validate event dates"""
    today = date.today()
    
    if start_date < today:
        raise EventValidationError("event_start_date", "Event cannot start in the past")
    
    if end_date < start_date:
        raise EventValidationError("event_end_date", "End date cannot be before start date")
    
    date_diff = (end_date - start_date).days
    if date_diff > 30:
        raise EventValidationError("event_end_date", "Event duration cannot exceed 30 days")
    
    return True
