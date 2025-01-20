from pydantic import BaseModel, Field, field_validator
from typing import Optional
from ..validations.financial_validator import (
    validate_salary, validate_allowance, validate_deduction,
    validate_bank_name, validate_account_name, validate_account_number,
    validate_iban, validate_salary_components, validate_allowance_total,
    validate_deduction_total
)

class UserFinancialInfoBase(BaseModel):
    user_id: Optional[str] = None
    salaryBasic: float = Field(gt=0)
    salaryGross: float = Field(gt=0)
    salaryNet: float = Field(gt=0)
    allowanceHouseRent: Optional[float] = Field(default=None, ge=0)
    allowanceMedical: Optional[float] = Field(default=None, ge=0)
    allowanceSpecial: Optional[float] = Field(default=None, ge=0)
    allowanceFuel: Optional[float] = Field(default=None, ge=0)
    allowancePhoneBill: Optional[float] = Field(default=None, ge=0)
    allowanceOther: Optional[float] = Field(default=None, ge=0)
    allowanceTotal: Optional[float] = Field(default=None, ge=0)
    deductionProvidentFund: Optional[float] = Field(default=None, ge=0)
    deductionTax: Optional[float] = Field(default=None, ge=0)
    deductionOther: Optional[float] = Field(default=None, ge=0)
    deductionTotal: Optional[float] = Field(default=None, ge=0)
    bankName: str
    accountName: str
    accountNumber: str
    iban: Optional[str] = None

    @field_validator('salaryBasic', 'salaryGross', 'salaryNet')
    @classmethod
    def validate_salary_amounts(cls, v, info):
        validate_salary(v, info.field_name)
        return v

    @field_validator('salaryGross')
    @classmethod
    def validate_gross_salary(cls, v, info):
        if 'salaryBasic' in info.data:
            validate_salary_components(info.data['salaryBasic'], v, info.data.get('salaryNet', 0))
        return v

    @field_validator('allowanceHouseRent', 'allowanceMedical', 'allowanceSpecial',
               'allowanceFuel', 'allowancePhoneBill', 'allowanceOther')
    @classmethod
    def validate_allowances(cls, v, info):
        if v is not None:
            validate_allowance(v, info.field_name)
        return v

    @field_validator('allowanceTotal')
    @classmethod
    def validate_total_allowance(cls, v, info):
        if v is not None:
            allowances = [
                info.data.get('allowanceHouseRent'), info.data.get('allowanceMedical'),
                info.data.get('allowanceSpecial'), info.data.get('allowanceFuel'),
                info.data.get('allowancePhoneBill'), info.data.get('allowanceOther')
            ]
            validate_allowance_total(allowances, v)
        return v

    @field_validator('deductionProvidentFund', 'deductionTax', 'deductionOther')
    @classmethod
    def validate_deductions(cls, v, info):
        if v is not None:
            validate_deduction(v, info.field_name)
        return v

    @field_validator('deductionTotal')
    @classmethod
    def validate_total_deduction(cls, v, info):
        if v is not None:
            deductions = [
                info.data.get('deductionProvidentFund'),
                info.data.get('deductionTax'),
                info.data.get('deductionOther')
            ]
            validate_deduction_total(deductions, v)
        return v

    @field_validator('bankName')
    @classmethod
    def validate_bank(cls, v):
        validate_bank_name(v)
        return v

    @field_validator('accountName')
    @classmethod
    def validate_account(cls, v):
        validate_account_name(v)
        return v

    @field_validator('accountNumber')
    @classmethod
    def validate_account_num(cls, v):
        validate_account_number(v)
        return v

    @field_validator('iban')
    @classmethod
    def validate_iban_format(cls, v):
        if v is not None:
            validate_iban(v)
        return v

class UserFinancialInfoCreate(UserFinancialInfoBase):
    pass

class UserFinancialInfoUpdate(BaseModel):
    salaryBasic: Optional[float] = None
    salaryGross: Optional[float] = None
    salaryNet: Optional[float] = None
    allowanceHouseRent: Optional[float] = None
    allowanceMedical: Optional[float] = None
    allowanceSpecial: Optional[float] = None
    allowanceFuel: Optional[float] = None
    allowancePhoneBill: Optional[float] = None
    allowanceOther: Optional[float] = None
    allowanceTotal: Optional[float] = None
    deductionProvidentFund: Optional[float] = None
    deductionTax: Optional[float] = None
    deductionOther: Optional[float] = None
    deductionTotal: Optional[float] = None
    bankName: Optional[str] = None
    accountName: Optional[str] = None
    accountNumber: Optional[str] = None
    iban: Optional[str] = None

    # Update validators to use field_validator
    @field_validator('salaryBasic', 'salaryGross', 'salaryNet')
    @classmethod
    def validate_salary_amounts(cls, v, info):
        if v is not None:
            validate_salary(v, info.field_name)
        return v

    @field_validator('allowanceHouseRent', 'allowanceMedical', 'allowanceSpecial',
                    'allowanceFuel', 'allowancePhoneBill', 'allowanceOther')
    @classmethod
    def validate_allowances(cls, v, info):
        if v is not None:
            validate_allowance(v, info.field_name)
        return v

    @field_validator('deductionProvidentFund', 'deductionTax', 'deductionOther')
    @classmethod
    def validate_deductions(cls, v, info):
        if v is not None:
            validate_deduction(v, info.field_name)
        return v

    @field_validator('bankName')
    @classmethod
    def validate_bank(cls, v):
        if v is not None:
            validate_bank_name(v)
        return v

    @field_validator('accountName')
    @classmethod
    def validate_account(cls, v):
        if v is not None:
            validate_account_name(v)
        return v

    @field_validator('accountNumber')
    @classmethod
    def validate_account_num(cls, v):
        if v is not None:
            validate_account_number(v)
        return v

    @field_validator('iban')
    @classmethod
    def validate_iban_format(cls, v):
        if v is not None:
            validate_iban(v)
        return v

class UserFinancialInfoResponse(UserFinancialInfoBase):
    financial_info_id: str

    class Config:
        orm_mode = True