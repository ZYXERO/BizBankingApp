from __future__ import annotations

from api_service.models.schemas import Account, AccountType, Customer


class InMemoryStore:
    customers: list[Customer] = []
    accounts: list[Account] = []
    seeded: bool = False

    @classmethod
    def seed_data(cls) -> None:
        if cls.seeded:
            return

        seed_customers = [
            ("Ayaan Khan", "ayaan@example.com"),
            ("Sara Ali", "sara@example.com"),
            ("Rahul Nair", "rahul@example.com"),
            ("Maya Patel", "maya@example.com"),
        ]
        for name, email in seed_customers:
            cls.customers.append(
                Customer(id=len(cls.customers) + 1, name=name, email=email)
            )

        seed_accounts = [
            (0, "ACC1001", AccountType.CHECKING, 4500.0),
            (1, "ACC1002", AccountType.SAVINGS, 12000.0),
            (2, "ACC1003", AccountType.CHECKING, 2200.0),
            (3, "ACC1004", AccountType.SAVINGS, 8700.0),
        ]
        for customer_index, account_number, account_type, balance in seed_accounts:
            cls.accounts.append(
                Account(
                    id=len(cls.accounts) + 1,
                    customer_id=cls.customers[customer_index].id,
                    account_number=account_number,
                    account_type=account_type,
                    balance=balance,
                )
            )
        cls._sync_customer_accounts()
        cls.seeded = True

    @classmethod
    def _reindex_ids(cls) -> None:
        """Keep customer and account ids as 1, 2, 3, ... in list order (no gaps)."""
        customer_id_map: dict[int, int] = {}
        for index, customer in enumerate(cls.customers, start=1):
            customer_id_map[customer.id] = index
            customer.id = index

        for account in cls.accounts:
            account.customer_id = customer_id_map.get(account.customer_id, account.customer_id)

        for index, account in enumerate(cls.accounts, start=1):
            account.id = index

        cls._sync_customer_accounts()

    @classmethod
    def _sync_customer_accounts(cls) -> None:
        customer_accounts: dict[int, list[Account]] = {customer.id: [] for customer in cls.customers}
        for account in cls.accounts:
            if account.customer_id in customer_accounts:
                customer_accounts[account.customer_id].append(account)
        for customer in cls.customers:
            customer.accounts = customer_accounts[customer.id]
