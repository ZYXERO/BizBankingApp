# BizBanking Backend API

FastAPI REST service for customers and accounts. Data is **in-memory only** (resets when the server process stops). IDs are kept sequential (`1`, `2`, `3`, ...) and renumbered after deletes.

## Run the API

```powershell
cd BizBankingApp
pip install -r requirements.txt
python -m uvicorn api_main:app --reload --host 127.0.0.1 --port 8000
```

- Root health: `GET http://127.0.0.1:8000/`
- Interactive docs: `http://127.0.0.1:8000/docs`

## Project layout (API)

```
api_main.py                 # App entry, routers, startup seed
api_service/
  controllers/              # HTTP routes
  services/                 # Business logic
  models/schemas.py         # Pydantic models
  data/store.py             # In-memory store + seed data
requirements.txt            # fastapi, uvicorn
```

## Seed data (on startup)

| Customer ID | Name        | Email              | Account ID | Number  | Type     | Balance |
|-------------|-------------|--------------------|------------|---------|----------|---------|
| 1           | Ayaan Khan  | ayaan@example.com  | 1          | ACC1001 | Checking | 4500    |
| 2           | Sara Ali    | sara@example.com   | 2          | ACC1002 | Savings  | 12000   |
| 3           | Rahul Nair  | rahul@example.com  | 3          | ACC1003 | Checking | 2200    |
| 4           | Maya Patel  | maya@example.com   | 4          | ACC1004 | Savings  | 8700    |

**Premium customers:** total balance across all accounts **greater than 10000**.

**Cascade delete:** deleting a customer removes that customer and all of their accounts.

**Create requests:** do not send `id` in the JSON body; the server assigns the next id.

## Endpoints

### System

| Method | Path | Status | Description |
|--------|------|--------|-------------|
| GET | `/` | 200 | API health message |

### Customers (`/api/customers`)

| Method | Path | Status | Description |
|--------|------|--------|-------------|
| GET | `/api/customers` | 200 | List all customers |
| GET | `/api/customers/premium` | 200 | Customers with total balance > 10000 |
| GET | `/api/customers/search?name=` | 200 | Search by name (partial match) |
| GET | `/api/customers/{customer_id}` | 200 / 404 | Get one customer |
| POST | `/api/customers` | 201 | Create customer |
| PUT | `/api/customers/{customer_id}` | 200 / 404 | Update customer |
| DELETE | `/api/customers/{customer_id}` | 204 / 404 | Delete customer and their accounts |

**POST / PUT body (customer):**

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

### Accounts (`/api/accounts`)

| Method | Path | Status | Description |
|--------|------|--------|-------------|
| GET | `/api/accounts` | 200 | List all accounts |
| GET | `/api/accounts/search?name=` | 200 | Accounts for customers matching name |
| GET | `/api/accounts/{account_id}` | 200 / 404 | Get one account |
| POST | `/api/accounts` | 201 / 404 | Create account (404 if customer missing) |
| PUT | `/api/accounts/{account_id}` | 200 / 404 | Update account |
| DELETE | `/api/accounts/{account_id}` | 204 / 404 | Delete account |

**POST body (create account):**

```json
{
  "customer_id": 1,
  "account_number": "ACC2001",
  "account_type": "Checking",
  "balance": 500.0
}
```

`account_type` must be `"Checking"` or `"Savings"`.

**PUT** uses the same fields as POST; the account id is in the URL (`/api/accounts/{account_id}`), not in the body.

## Postman tips

- Set environment variable `baseUrl` = `http://127.0.0.1:8000`
- Use **raw JSON** for POST and PUT; no body for DELETE
- After a full server restart, seed ids are **1-4** for both customers and accounts

## Service-layer tests

- [TESTING.md](TESTING.md) — assertions, how to run `pytest`, green/red in Cursor
- [TEST-CASES.md](TEST-CASES.md) — every test case in markdown tables
- Code: `tests/` (run `pytest -v`)

## Branch

Console app: `main`  
Backend API: `bank-app-backend-api-service`
