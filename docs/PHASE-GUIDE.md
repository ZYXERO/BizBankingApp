# Student Guide — Repo Mapping

How each guide step maps to this project.

## Phase 1 — Object blueprints

| Step | Guide task | In this repo |
|------|------------|--------------|
| 1 | `ITransaction` + `PrintReceipt` | `models/itransaction.py` |
| 2 | `Customer` class | `models/customer.py` |
| 3 | Abstract `Account` | `models/account.py` |
| 4 | `SavingsAccount` | `models/savings_account.py` |
| 5 | `CheckingAccount` | `models/checking_account.py` |

**Concepts:** abstraction, encapsulation, inheritance, polymorphism (`withdraw` differs per type).

## Phase 2 — Control flow and data

| Step | Guide task | In this repo |
|------|------------|--------------|
| 6 | Seed 2–3 customers | `storage.py` → `seed()` |
| 7 | Master menu loop | `app.py` → `master_menu()` + `menu_loop()` |
| 8 | Create + view accounts | `create_account()`, `view` in master menu |
| 9 | Deposit + withdraw | `deposit()`, `withdraw()` + model calls |
| 10 | Transfer | `transfer()` |
| 11 | Close account | `close_account()` |

**Concepts:** loops, lists, single console flow.

## Phase 3 — Hardening and polish

| Step | Guide task | In this repo |
|------|------------|--------------|
| 12 | try/except, invalid input | `read_money()`, `read_int()`, `run_block()` |
| 13 | Layout + receipts | `ui.section()`, `Account.print_receipt()` |

## Suggested demo order (for presentation)

1. Show `models/` — explain OOP structure  
2. Run app — login as `sara` / `sara123`  
3. View accounts → deposit → show receipt  
4. Withdraw from savings — show $100 minimum rule  
5. Optional: admin login, add customer  

See [THOUGHT-FLOW.md](THOUGHT-FLOW.md) for visual flows.
