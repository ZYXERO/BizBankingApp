# Service-layer testing guide

Assignment requirement (Rohit): write test cases for **all methods** in the **service layer** — at least **one success** and **one failure** per method.

- Code: `tests/test_customer_service.py`, `tests/test_account_service.py`
- Written catalog: [TEST-CASES.md](TEST-CASES.md) (every scenario in tables)
- Config: `pytest.ini`

---

## What is an assertion?

An **assertion** is a check in a test that says: *this must be true*.

```python
assert len(customers) == 4
```

| Result | Meaning |
|--------|---------|
| Condition is **true** | Test **passes** (green) |
| Condition is **false** | Test **fails** (red); pytest prints what went wrong |

Tests call a **service method**, then use `assert` on the return value or side effect. We are **not** testing HTTP/Postman here — only `CustomerService` and `AccountService`.

---

## Common assertion types (Python / pytest)

| Type | Example | When to use |
|------|---------|-------------|
| Equality | `assert x == 4` | Exact match (count, id, string) |
| Inequality | `assert x != 0` | Must differ |
| Comparison | `assert balance > 10000` | Premium threshold, ranges |
| Truthy / falsy | `assert result` / `assert not result` | `delete_*` returns `True`/`False` |
| `is None` / `is not None` | `assert customer is None` | Not found vs found |
| Membership | `assert "Sara" in names` | Search / premium lists |
| Empty collection | `assert results == []` | No matches |
| Type | `assert isinstance(x, Customer)` | Return type checks |
| Approximate float | `assert x == pytest.approx(100.0)` | Money with decimals |
| Exception | `with pytest.raises(ValidationError):` | Invalid Pydantic input |

Your project already uses most of these. See [TEST-CASES.md](TEST-CASES.md) for the exact assertion per scenario.

---

## How to run tests

From the project root:

```powershell
pip install -r requirements.txt
pytest
```

Verbose (recommended for demos):

```powershell
pytest -v
```

Expected: **28 passed** (as of current suite).

---

## Green / red in Cursor or VS Code

1. Install the **Python** extension.
2. `Ctrl+Shift+P` → **Python: Configure Tests** → **pytest** → root **`.`**
3. Open **Testing** (beaker icon in the sidebar).
4. Run all tests or a single test — pass = green, fail = red.

Terminal output also shows `PASSED` / `FAILED`.

---

## Test layout

```
tests/
  conftest.py                 # seeded_store / empty_store fixtures
  test_customer_service.py    # CustomerService methods
  test_account_service.py     # AccountService methods
```

**Why `tests/` and not `src/test`?**  
The API services live in `api_service/services/`. The console app lives in `src/`. Root-level `tests/` is standard for pytest and matches this API branch.

Fixtures reset the in-memory store before each test so tests do not affect each other.

---

## Success vs failure scenarios

| Scenario | Idea | Example in this project |
|----------|------|-------------------------|
| **Success** | Method works with valid data | Get customer id `1` → name and email match seed |
| **Failure** | Method handles bad/missing data | Get customer id `999` → `None` |

Some failures are **validation** (empty name, short account number) — Pydantic raises `ValidationError` before the service runs.

---

## Scope (today vs tomorrow)

| Today | Tomorrow (per class plan) |
|-------|---------------------------|
| Service layer only (`pytest`) | MongoDB Atlas connection |
| In-memory store in tests | React frontend (optional MySQL) |

Controller/HTTP tests and Postman are separate from this pytest suite.

---

## Related docs

- [TEST-CASES.md](TEST-CASES.md) — full list of test cases and assertions
- [API.md](API.md) — REST API and how to run the server
