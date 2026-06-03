from __future__ import annotations

import pytest
from pydantic import ValidationError

from api_service.models.schemas import CreateCustomerRequest, UpdateCustomerRequest
from api_service.services.account_service import AccountService
from api_service.services.customer_service import CustomerService


class TestGetAllCustomers:
  def test_success_returns_seeded_customers(self, seeded_store: None) -> None:
    customers = CustomerService.get_all_customers()
    assert len(customers) == 4
    assert customers[0].name == "Ayaan Khan"

  def test_failure_returns_empty_list_when_store_empty(self, empty_store: None) -> None:
    assert CustomerService.get_all_customers() == []


class TestGetCustomerById:
  def test_success_finds_existing_customer(self, seeded_store: None) -> None:
    customer = CustomerService.get_customer_by_id(1)
    assert customer is not None
    assert customer.email == "ayaan@example.com"

  def test_failure_returns_none_for_missing_id(self, seeded_store: None) -> None:
    assert CustomerService.get_customer_by_id(999) is None


class TestSearchCustomersByName:
  def test_success_finds_partial_name_match(self, seeded_store: None) -> None:
    results = CustomerService.search_customers_by_name("sara")
    assert len(results) == 1
    assert results[0].name == "Sara Ali"

  def test_failure_returns_empty_when_no_match(self, seeded_store: None) -> None:
    assert CustomerService.search_customers_by_name("not-a-real-name") == []


class TestGetAllPremiumCustomers:
  def test_success_returns_customers_over_threshold(self, seeded_store: None) -> None:
    premium = CustomerService.get_all_premium_customers()
    names = {customer.name for customer in premium}
    assert "Sara Ali" in names

  def test_failure_returns_empty_when_no_one_is_premium(self, seeded_store: None) -> None:
    from api_service.data.store import InMemoryStore

    InMemoryStore.accounts.clear()
    InMemoryStore._sync_customer_accounts()
    assert CustomerService.get_all_premium_customers() == []


class TestCreateCustomer:
  def test_success_appends_customer_with_next_id(self, seeded_store: None) -> None:
    created = CustomerService.create_customer(
      CreateCustomerRequest(name="New User", email="new@example.com")
    )
    assert created.id == 5
    assert CustomerService.get_customer_by_id(5) is not None

  def test_failure_rejects_invalid_request_before_service(self) -> None:
    with pytest.raises(ValidationError):
      CreateCustomerRequest(name="", email="bad@example.com")


class TestUpdateCustomer:
  def test_success_updates_name_and_email(self, seeded_store: None) -> None:
    updated = CustomerService.update_customer(
      1,
      UpdateCustomerRequest(name="Ayaan Updated", email="ayaan.new@example.com"),
    )
    assert updated is not None
    assert updated.name == "Ayaan Updated"

  def test_failure_returns_none_for_missing_customer(self, seeded_store: None) -> None:
    result = CustomerService.update_customer(
      999,
      UpdateCustomerRequest(name="Ghost", email="ghost@example.com"),
    )
    assert result is None


class TestDeleteCustomer:
  def test_success_removes_customer_and_their_accounts(self, seeded_store: None) -> None:
    assert CustomerService.delete_customer(1) is True
    names = {customer.name for customer in CustomerService.get_all_customers()}
    assert "Ayaan Khan" not in names
    assert "ACC1001" not in {a.account_number for a in AccountService.get_all_accounts()}
    assert len(names) == 3

  def test_failure_returns_false_for_missing_customer(self, seeded_store: None) -> None:
    assert CustomerService.delete_customer(999) is False
