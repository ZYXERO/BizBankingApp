from decimal import Decimal

from models.account import Account
from models.customer import Customer


class CheckingAccount(Account):
    def __init__(self, account_number: str, account_holder: Customer, balance: Decimal, overdraft_limit: Decimal) -> None:
        super().__init__(account_number, account_holder, balance)
        self._overdraft_limit = overdraft_limit

    @property
    def overdraft_limit(self) -> Decimal:
        return self._overdraft_limit

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0 or self._balance - amount < -self._overdraft_limit:
            return False
        self._balance -= amount
        self._last_transaction_type = "WITHDRAW"
        self._last_transaction_amount = amount
        return True
