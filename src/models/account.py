from __future__ import annotations

from abc import abstractmethod
from decimal import Decimal

from models.customer import Customer
from models.itransaction import ITransaction


class Account(ITransaction):
    def __init__(self, account_number: str, account_holder: Customer, balance: Decimal) -> None:
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = balance
        self._last_transaction_type = "NONE"
        self._last_transaction_amount = Decimal("0")

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def account_holder(self) -> Customer:
        return self._account_holder

    @property
    def balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal) -> bool:
        if amount <= 0:
            return False
        self._balance += amount
        self._last_transaction_type = "DEPOSIT"
        self._last_transaction_amount = amount
        return True

    @abstractmethod
    def withdraw(self, amount: Decimal) -> bool:
        pass

    def print_receipt(self) -> None:
        print("---------- Transaction Receipt ----------")
        print(f"Account Number : {self._account_number}")
        print(f"Account Holder : {self._account_holder}")
        print(f"Account Type   : {self.__class__.__name__}")
        print(f"Transaction    : {self._last_transaction_type}")
        print(f"Amount         : ${self._last_transaction_amount:.2f}")
        print(f"Balance        : ${self._balance:.2f}")
        print("-----------------------------------------")
