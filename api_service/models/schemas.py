from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class AccountType(str, Enum):
    SAVINGS = "Savings"
    CHECKING = "Checking"


class Account(BaseModel):
    id: int
    customer_id: int
    account_number: str
    account_type: AccountType
    balance: float = Field(ge=0)


class Customer(BaseModel):
    id: int
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    accounts: List[Account] = Field(default_factory=list)


class CreateCustomerRequest(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)


class UpdateCustomerRequest(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)


class CreateAccountRequest(BaseModel):
    customer_id: int
    account_number: str = Field(min_length=3)
    account_type: AccountType
    balance: float = Field(ge=0)


class UpdateAccountRequest(BaseModel):
    customer_id: int
    account_number: str = Field(min_length=3)
    account_type: AccountType
    balance: float = Field(ge=0)


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detail: str
