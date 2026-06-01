from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.account import Account


class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str) -> None:
        self._customer_id = customer_id
        self._first_name = first_name
        self._last_name = last_name
        self._accounts: list[Account] = []

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def accounts(self) -> list[Account]:
        return self._accounts

    def add_account(self, account: Account) -> None:
        self._accounts.append(account)

    def __str__(self) -> str:
        return f"{self._first_name} {self._last_name} (ID: {self._customer_id})"
