from __future__ import annotations

from api_service.data.store import InMemoryStore
from api_service.models.schemas import Account, CreateAccountRequest, UpdateAccountRequest


class AccountService:
    @staticmethod
    def get_all_accounts() -> list[Account]:
        return InMemoryStore.accounts

    @staticmethod
    def get_account_by_id(account_id: int) -> Account | None:
        return next((account for account in InMemoryStore.accounts if account.id == account_id), None)

    @staticmethod
    def search_accounts_by_customer_name(name: str) -> list[Account]:
        target = name.strip().lower()
        matching_customer_ids = {
            customer.id for customer in InMemoryStore.customers if target in customer.name.lower()
        }
        return [account for account in InMemoryStore.accounts if account.customer_id in matching_customer_ids]

    @staticmethod
    def create_account(payload: CreateAccountRequest) -> Account | None:
        customer_exists = any(customer.id == payload.customer_id for customer in InMemoryStore.customers)
        if not customer_exists:
            return None

        account = Account(
            id=len(InMemoryStore.accounts) + 1,
            customer_id=payload.customer_id,
            account_number=payload.account_number.strip(),
            account_type=payload.account_type,
            balance=payload.balance,
        )
        InMemoryStore.accounts.append(account)
        InMemoryStore._sync_customer_accounts()
        return account

    @staticmethod
    def update_account(account_id: int, payload: UpdateAccountRequest) -> Account | None:
        account = AccountService.get_account_by_id(account_id)
        if account is None:
            return None

        customer_exists = any(customer.id == payload.customer_id for customer in InMemoryStore.customers)
        if not customer_exists:
            return None

        account.customer_id = payload.customer_id
        account.account_number = payload.account_number.strip()
        account.account_type = payload.account_type
        account.balance = payload.balance
        InMemoryStore._sync_customer_accounts()
        return account

    @staticmethod
    def delete_account(account_id: int) -> bool:
        account = AccountService.get_account_by_id(account_id)
        if account is None:
            return False
        InMemoryStore.accounts = [item for item in InMemoryStore.accounts if item.id != account_id]
        InMemoryStore._reindex_ids()
        return True
