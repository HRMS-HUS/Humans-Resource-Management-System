class UserValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        return {
            "field": self.field,
            "message": self.message
        }

class EventValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field,
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        return {
            "field": self.field,
            "message": self.message
        }

class FinancialValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        return {
            "field": self.field,
            "message": self.message
        }

