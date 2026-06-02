from __future__ import annotations

from api_service.data.store import InMemoryStore
from api_service.models.schemas import CreateCustomerRequest, Customer, UpdateCustomerRequest

PREMIUM_THRESHOLD = 10000.0


class CustomerService:
    @staticmethod
    def get_all_customers() -> list[Customer]:
        return InMemoryStore.customers

    @staticmethod
    def get_customer_by_id(customer_id: int) -> Customer | None:
        return next((customer for customer in InMemoryStore.customers if customer.id == customer_id), None)

    @staticmethod
    def search_customers_by_name(name: str) -> list[Customer]:
        target = name.strip().lower()
        return [customer for customer in InMemoryStore.customers if target in customer.name.lower()]

    @staticmethod
    def get_all_premium_customers() -> list[Customer]:
        premium_customers: list[Customer] = []
        for customer in InMemoryStore.customers:
            total_balance = sum(account.balance for account in customer.accounts)
            if total_balance > PREMIUM_THRESHOLD:
                premium_customers.append(customer)
        return premium_customers

    @staticmethod
    def create_customer(payload: CreateCustomerRequest) -> Customer:
        customer = Customer(
            id=len(InMemoryStore.customers) + 1,
            name=payload.name.strip(),
            email=payload.email.strip(),
        )
        InMemoryStore.customers.append(customer)
        return customer

    @staticmethod
    def update_customer(customer_id: int, payload: UpdateCustomerRequest) -> Customer | None:
        customer = CustomerService.get_customer_by_id(customer_id)
        if customer is None:
            return None
        customer.name = payload.name.strip()
        customer.email = payload.email.strip()
        return customer

    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        customer = CustomerService.get_customer_by_id(customer_id)
        if customer is None:
            return False

        InMemoryStore.customers = [item for item in InMemoryStore.customers if item.id != customer_id]
        InMemoryStore.accounts = [account for account in InMemoryStore.accounts if account.customer_id != customer_id]
        InMemoryStore._reindex_ids()
        return True
