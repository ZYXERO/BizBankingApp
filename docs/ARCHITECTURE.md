# Architecture

Simple layout: **console UI** → **app logic** → **storage (lists/dicts)** + **OOP models (rules + receipts)**.

## Module map

```mermaid
flowchart LR
    subgraph entry [Entry]
        MP[Main.py]
    end
    subgraph core [Application]
        APP[app.py BizBankingApp]
        UI[ui.py menus + input]
        ST[storage.py DataStore]
    end
    subgraph oop [Phase 1 Models]
        IT[ITransaction]
        CU[Customer]
        AC[Account abstract]
        SV[SavingsAccount]
        CH[CheckingAccount]
    end
    subgraph files [Files]
        JSON[bizbanking_data.json]
        LOG[bizbanking_register.log]
    end
    MP --> APP
    APP --> UI
    APP --> ST
    APP --> oop
    ST --> JSON
    ST --> LOG
```

## Class diagram (OOP)

```mermaid
classDiagram
    class ITransaction {
        <<interface>>
        +print_receipt()
    }
    class Customer {
        -_customer_id
        -_first_name
        -_last_name
        -_accounts
        +add_account()
    }
    class Account {
        <<abstract>>
        -_account_number
        -_account_holder
        -_balance
        +deposit()
        +withdraw()*
        +print_receipt()
    }
    class SavingsAccount {
        -_interest_rate
        +withdraw()
    }
    class CheckingAccount {
        -_overdraft_limit
        +withdraw()
    }
    ITransaction <|.. Account
    Account <|-- SavingsAccount
    Account <|-- CheckingAccount
    Customer "1" --> "*" Account : holds
    Account --> Customer : account_holder
```

## Who does what

| File | Role |
|------|------|
| `Main.py` | Starts the app |
| `app.py` | Menus, login, transactions, calls models |
| `ui.py` | Print sections, read input, parse menu text |
| `storage.py` | Load/save JSON, seed data, register log |
| `models/*` | OOP rules and receipts (Phase 1) |
