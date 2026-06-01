# BizBanking

A terminal-based banking application built with Python. The project follows a step-by-step design: **OOP class blueprints**, **menu-driven banking operations**, and **input validation with transaction receipts**.

## Objective

Build an interactive console banking app that practices:

- Variables, loops, lists, and exception handling  
- Object-oriented programming: **classes**, **encapsulation**, **inheritance**, **polymorphism**, and **abstraction**

---

## Project Phases

### Phase 1 — Structural object blueprints (`models/`)

| Step | Component | Purpose |
|------|-----------|---------|
| 1 | `ITransaction` | Contract for `print_receipt()` |
| 2 | `Customer` | Customer ID, name, list of accounts (encapsulation) |
| 3 | `Account` (abstract) | Shared fields, `deposit()`, abstract `withdraw()` |
| 4 | `SavingsAccount` | Interest rate; withdraw cannot go below **$100** |
| 5 | `CheckingAccount` | Overdraft limit; withdraw allowed within overdraft |

### Phase 2 — Control flow and data management

| Step | Feature |
|------|---------|
| 6 | Seed default customers and accounts on first run |
| 7 | Master menu loop after login |
| 8 | Create account, view accounts (CRUD-style) |
| 9 | Deposit and withdraw using **polymorphic** account rules |
| 10 | Transfer between accounts |
| 11 | Close account |

**Master menu (customer login):**

1. Create Account  
2. View All Accounts  
3. Deposit  
4. Withdraw  
5. Transfer  
6. Close Account  
7. Logout  

### Phase 3 — Hardening and polish

| Step | Feature |
|------|---------|
| 12 | Try/except for invalid numbers and bad input |
| 13 | Clear console sections and **transaction receipts** after operations |

---

## Project structure

```
BizBankingApp/
├── Main.py              # Run the app
├── app.py               # Main application logic
├── ui.py                # Console menus and input
├── storage.py           # JSON file storage
├── models/              # Phase 1 OOP classes
│   ├── itransaction.py
│   ├── customer.py
│   ├── account.py
│   ├── savings_account.py
│   └── checking_account.py
├── bizbanking_data.json # Saved customers (created at runtime)
└── bizbanking_register.log
```

---

## Requirements

- Python 3.10+ (tested on 3.14)
- No extra pip packages (stdlib only: `json`, `os`, `decimal`, `re`, etc.)

---

## How to run

```bash
cd BizBankingApp
python Main.py
```

Main screen:

- `1` or `login` — sign in  
- `2` or `register` — new customer  
- `3` or `exit` — quit  
- **Esc** on the welcome screen also exits (Windows)

Flexible input works on menus (examples: `1`, `1.`, `1 login`, `3 deposit`).

---

## Test accounts

**Seeded users (first run):**

| Username | Password | Notes |
|----------|----------|--------|
| `ayaan` | `ayaan123` | Checking account |
| `sara` | `sara123` | Savings account |

**Admin:**

| Username | Password |
|----------|------------|
| `admin` | `bruhImTheAdmin` |

Admin menu: manage customers, add accounts, view all accounts and transactions.

You can also **Register** to create your own customer, then use the master menu.

---

## Data storage

- `bizbanking_data.json` — customers, accounts, transactions  
- `bizbanking_register.log` — registration log entries  

Copy the project folder (including the JSON file) to move data to another machine.

---

## OOP in practice

When you deposit, withdraw, or transfer, the app builds a `SavingsAccount` or `CheckingAccount` object and calls its methods. Each account type applies its own **withdraw** rules (polymorphism), then prints a receipt via `ITransaction`.

---

## Author

Collabera Training — Banking App Console Project
