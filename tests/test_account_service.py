from __future__ import annotations

import pytest
from pydantic import ValidationError

from api_service.models.schemas import AccountType, CreateAccountRequest, UpdateAccountRequest
from api_service.services.account_service import AccountService


class TestGetAllAccounts:
  def test_success_returns_seeded_accounts(self, seeded_store: None) -> None:
    accounts = AccountService.get_all_accounts()
    assert len(accounts) == 4
    assert accounts[0].account_number == "ACC1001"

  def test_failure_returns_empty_list_when_store_empty(self, empty_store: None) -> None:
    assert AccountService.get_all_accounts() == []


class TestGetAccountById:
  def test_success_finds_existing_account(self, seeded_store: None) -> None:
    account = AccountService.get_account_by_id(1)
    assert account is not None
    assert account.customer_id == 1

  def test_failure_returns_none_for_missing_id(self, seeded_store: None) -> None:
    assert AccountService.get_account_by_id(999) is None


class TestSearchAccountsByCustomerName:
  def test_success_finds_accounts_for_matching_customer(self, seeded_store: None) -> None:
    results = AccountService.search_accounts_by_customer_name("maya")
    assert len(results) == 1
    assert results[0].account_number == "ACC1004"

  def test_failure_returns_empty_when_no_customer_matches(self, seeded_store: None) -> None:
    assert AccountService.search_accounts_by_customer_name("unknown") == []


class TestCreateAccount:
  def test_success_creates_account_for_existing_customer(self, seeded_store: None) -> None:
    created = AccountService.create_account(
      CreateAccountRequest(
        customer_id=1,
        account_number="ACC9001",
        account_type=AccountType.CHECKING,
        balance=250.0,
      )
    )
    assert created is not None
    assert created.id == 5
    assert created.customer_id == 1

  def test_failure_returns_none_when_customer_does_not_exist(self, seeded_store: None) -> None:
    result = AccountService.create_account(
      CreateAccountRequest(
        customer_id=999,
        account_number="ACC9002",
        account_type=AccountType.SAVINGS,
        balance=100.0,
      )
    )
    assert result is None


class TestUpdateAccount:
  def test_success_updates_account_fields(self, seeded_store: None) -> None:
    updated = AccountService.update_account(
      1,
      UpdateAccountRequest(
        customer_id=1,
        account_number="ACC1001X",
        account_type=AccountType.SAVINGS,
        balance=5000.0,
      ),
    )
    assert updated is not None
    assert updated.account_number == "ACC1001X"
    assert updated.balance == 5000.0

  def test_failure_returns_none_for_missing_account(self, seeded_store: None) -> None:
    result = AccountService.update_account(
      999,
      UpdateAccountRequest(
        customer_id=1,
        account_number="ACC9999",
        account_type=AccountType.CHECKING,
        balance=1.0,
      ),
    )
    assert result is None

  def test_failure_returns_none_when_target_customer_missing(self, seeded_store: None) -> None:
    result = AccountService.update_account(
      1,
      UpdateAccountRequest(
        customer_id=999,
        account_number="ACC1001",
        account_type=AccountType.CHECKING,
        balance=100.0,
      ),
    )
    assert result is None


class TestDeleteAccount:
  def test_success_removes_account(self, seeded_store: None) -> None:
    assert AccountService.delete_account(1) is True
    numbers = {account.account_number for account in AccountService.get_all_accounts()}
    assert "ACC1001" not in numbers
    assert len(numbers) == 3

  def test_failure_returns_false_for_missing_account(self, seeded_store: None) -> None:
    assert AccountService.delete_account(999) is False


class TestCreateAccountValidation:
  def test_failure_rejects_short_account_number(self) -> None:
    with pytest.raises(ValidationError):
      CreateAccountRequest(
        customer_id=1,
        account_number="AB",
        account_type=AccountType.CHECKING,
        balance=10.0,
      )
