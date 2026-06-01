from decimal import Decimal

from models.account import Account
from models.customer import Customer


class SavingsAccount(Account):
    MINIMUM_BALANCE = Decimal("100")

    def __init__(self, account_number: str, account_holder: Customer, balance: Decimal, interest_rate: Decimal) -> None:
        super().__init__(account_number, account_holder, balance)
        self._interest_rate = interest_rate

    @property
    def interest_rate(self) -> Decimal:
        return self._interest_rate

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0 or self._balance - amount < self.MINIMUM_BALANCE:
            return False
        self._balance -= amount
        self._last_transaction_type = "WITHDRAW"
        self._last_transaction_amount = amount
        return True
