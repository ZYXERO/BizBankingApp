# Service-layer test case catalog

This document lists every automated test case. The **executable** tests are in `tests/`; this file is the **written spec** for review or submission.

**Total:** 28 tests (14 service methods covered; `update_account` has two failure cases).

Run: `pytest -v` from project root.

---

## CustomerService (`api_service/services/customer_service.py`)

### `get_all_customers`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-01 | Success | `test_success_returns_seeded_customers` | Seeded store | `get_all_customers()` | `len == 4`; first name is `Ayaan Khan` |
| C-02 | Failure | `test_failure_returns_empty_list_when_store_empty` | Empty store | `get_all_customers()` | Returns `[]` |

### `get_customer_by_id`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-03 | Success | `test_success_finds_existing_customer` | Seeded | `get_customer_by_id(1)` | Not `None`; email `ayaan@example.com` |
| C-04 | Failure | `test_failure_returns_none_for_missing_id` | Seeded | `get_customer_by_id(999)` | `None` |

### `search_customers_by_name`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-05 | Success | `test_success_finds_partial_name_match` | Seeded | `search_customers_by_name("sara")` | One result; name `Sara Ali` |
| C-06 | Failure | `test_failure_returns_empty_when_no_match` | Seeded | `search_customers_by_name("not-a-real-name")` | `[]` |

### `get_all_premium_customers`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-07 | Success | `test_success_returns_customers_over_threshold` | Seeded | `get_all_premium_customers()` | `Sara Ali` in result (total balance > 10000) |
| C-08 | Failure | `test_failure_returns_empty_when_no_one_is_premium` | Seeded, then clear all accounts | `get_all_premium_customers()` | `[]` |

### `create_customer`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-09 | Success | `test_success_appends_customer_with_next_id` | Seeded | Create `New User` / `new@example.com` | `id == 5`; customer exists |
| C-10 | Failure | `test_failure_rejects_invalid_request_before_service` | None | `CreateCustomerRequest(name="")` | Raises `ValidationError` |

### `update_customer`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-11 | Success | `test_success_updates_name_and_email` | Seeded | Update customer `1` | Not `None`; name `Ayaan Updated` |
| C-12 | Failure | `test_failure_returns_none_for_missing_customer` | Seeded | Update customer `999` | `None` |

### `delete_customer`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| C-13 | Success | `test_success_removes_customer_and_their_accounts` | Seeded | `delete_customer(1)` | Returns `True`; `Ayaan Khan` gone; `ACC1001` gone; 3 customers left |
| C-14 | Failure | `test_failure_returns_false_for_missing_customer` | Seeded | `delete_customer(999)` | `False` |

**File:** `tests/test_customer_service.py`

---

## AccountService (`api_service/services/account_service.py`)

### `get_all_accounts`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-01 | Success | `test_success_returns_seeded_accounts` | Seeded | `get_all_accounts()` | `len == 4`; first number `ACC1001` |
| A-02 | Failure | `test_failure_returns_empty_list_when_store_empty` | Empty store | `get_all_accounts()` | `[]` |

### `get_account_by_id`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-03 | Success | `test_success_finds_existing_account` | Seeded | `get_account_by_id(1)` | Not `None`; `customer_id == 1` |
| A-04 | Failure | `test_failure_returns_none_for_missing_id` | Seeded | `get_account_by_id(999)` | `None` |

### `search_accounts_by_customer_name`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-05 | Success | `test_success_finds_accounts_for_matching_customer` | Seeded | `search_accounts_by_customer_name("maya")` | One account; `ACC1004` |
| A-06 | Failure | `test_failure_returns_empty_when_no_customer_matches` | Seeded | `search_accounts_by_customer_name("unknown")` | `[]` |

### `create_account`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-07 | Success | `test_success_creates_account_for_existing_customer` | Seeded | Create for `customer_id=1`, `ACC9001` | Not `None`; `id == 5`; `customer_id == 1` |
| A-08 | Failure | `test_failure_returns_none_when_customer_does_not_exist` | Seeded | Create for `customer_id=999` | `None` |

### `update_account`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-09 | Success | `test_success_updates_account_fields` | Seeded | Update account `1` | Not `None`; number `ACC1001X`; balance `5000.0` |
| A-10 | Failure | `test_failure_returns_none_for_missing_account` | Seeded | Update account `999` | `None` |
| A-10b | Failure | `test_failure_returns_none_when_target_customer_missing` | Seeded | Update account `1` with `customer_id=999` | `None` |

### `delete_account`

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-11 | Success | `test_success_removes_account` | Seeded | `delete_account(1)` | `True`; `ACC1001` not in list; 3 accounts remain |
| A-12 | Failure | `test_failure_returns_false_for_missing_account` | Seeded | `delete_account(999)` | `False` |

### CreateAccountRequest validation (supports `create_account`)

| ID | Type | Test name | Setup | Action | Expected (assertions) |
|----|------|-----------|-------|--------|------------------------|
| A-13 | Failure | `test_failure_rejects_short_account_number` | None | `account_number="AB"` | Raises `ValidationError` |

**File:** `tests/test_account_service.py`

---

## Coverage summary

| Service class | Methods | Success tests | Failure tests |
|---------------|---------|---------------|---------------|
| CustomerService | 7 | 7 | 7 |
| AccountService | 6 | 6 | 8 (extra failure on `update_account` + validation) |

---

## Seed data used by `seeded_store` fixture

| Customer ID | Name | Account ID | Number | Balance |
|-------------|------|------------|--------|---------|
| 1 | Ayaan Khan | 1 | ACC1001 | 4500 |
| 2 | Sara Ali | 2 | ACC1002 | 12000 |
| 3 | Rahul Nair | 3 | ACC1003 | 2200 |
| 4 | Maya Patel | 4 | ACC1004 | 8700 |

Premium rule: sum of customer account balances **> 10000** (Sara qualifies with seed data).

---

## Related

- [TESTING.md](TESTING.md) — what assertions are, how to run pytest, green/red in IDE
- [API.md](API.md) — REST API reference
