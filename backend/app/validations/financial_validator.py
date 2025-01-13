from ..providers.validation_exceptions import FinancialValidationError
import re

def validate_salary(salary: float, field_name: str) -> bool:
    """Validate salary amount (must be positive)"""
    if salary < 0:
        raise FinancialValidationError(field_name, f"{field_name} cannot be negative")
    return True

def validate_allowance(allowance: float, field_name: str) -> bool:
    """Validate allowance amount (must be zero or positive)"""
    if allowance < 0:
        raise FinancialValidationError(field_name, f"{field_name} cannot be negative")
    return True

def validate_deduction(deduction: float, field_name: str) -> bool:
    """Validate deduction amount (must be zero or positive)"""
    if deduction < 0:
        raise FinancialValidationError(field_name, f"{field_name} cannot be negative")
    return True

def validate_bank_name(bank_name: str) -> bool:
    """Validate bank name"""
    if not (2 <= len(bank_name) <= 100):
        raise FinancialValidationError("bank_name", "Bank name must be between 2 and 100 characters")
    if not re.match(r'^[a-zA-Z\s\'-]+$', bank_name):
        raise FinancialValidationError("bank_name", "Bank name contains invalid characters")
    return True

def validate_account_name(account_name: str) -> bool:
    """Validate account holder name"""
    if not (2 <= len(account_name) <= 100):
        raise FinancialValidationError("account_name", "Account name must be between 2 and 100 characters")
    if not re.match(r'^[a-zA-Z\s\'-]+$', account_name):
        raise FinancialValidationError("account_name", "Account name contains invalid characters")
    return True

def validate_account_number(account_number: str) -> bool:
    """Validate bank account number"""
    if not re.match(r'^[0-9]{8,20}$', account_number):
        raise FinancialValidationError("account_number", "Account number must contain 8-20 digits only")
    return True

def validate_iban(iban: str) -> bool:
    """Validate IBAN format"""
    if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{4,32}$', iban):
        raise FinancialValidationError("iban", "Invalid IBAN format")
    return True

def validate_salary_components(basic: float, gross: float, net: float) -> bool:
    """Validate salary components relationships"""
    if not (basic <= gross):
        raise FinancialValidationError("salary", "Basic salary cannot be greater than gross salary")
    if not (net <= gross):
        raise FinancialValidationError("salary", "Net salary cannot be greater than gross salary")
    return True

def validate_allowance_total(individual_allowances: list[float], total: float) -> bool:
    """Validate if total allowance matches sum of individual allowances"""
    calculated_total = sum(allowance for allowance in individual_allowances if allowance is not None)
    if abs(calculated_total - total) > 0.01:  # Using 0.01 to handle floating point precision
        raise FinancialValidationError("allowance_total", "Total allowance doesn't match sum of individual allowances")
    return True

def validate_deduction_total(individual_deductions: list[float], total: float) -> bool:
    """Validate if total deduction matches sum of individual deductions"""
    calculated_total = sum(deduction for deduction in individual_deductions if deduction is not None)
    if abs(calculated_total - total) > 0.01:  # Using 0.01 to handle floating point precision
        raise FinancialValidationError("deduction_total", "Total deduction doesn't match sum of individual deductions")
    return True
