# BizBanking — Thought Flow

High-level path from starting the app to finishing a transaction.

## 1. Application startup

```mermaid
flowchart TD
    A[Start: python main.py] --> B[Load data/bizbanking_data.json]
    B --> C{File exists?}
    C -->|No| D[Seed demo users: ayaan, sara]
    C -->|Yes| E[Read customers + transactions]
    D --> F[Show Welcome to BizBanking]
    E --> F
    F --> G[Main menu loop]
```

## 2. Main menu (before login)

```mermaid
flowchart TD
    M[Main Menu] --> L[1 Login]
    M --> R[2 Register]
    M --> X[3 Exit / Esc]
    L --> C[Enter username + password]
    R --> REG[Register new customer]
    X --> END[Goodbye - stop app]
    C --> AUTH{Valid?}
    AUTH -->|Admin| ADM[Admin Dashboard]
    AUTH -->|Customer| CUST[Master Menu]
    AUTH -->|Invalid| M
    REG --> M
    ADM --> M
    CUST --> M
```

## 3. Customer master menu (Phase 2)

```mermaid
flowchart TD
    MM[Master Menu] --> A1[1 Create Account]
    MM --> A2[2 View All Accounts]
    MM --> A3[3 Deposit]
    MM --> A4[4 Withdraw]
    MM --> A5[5 Transfer]
    MM --> A6[6 Close Account]
    MM --> A7[7 Logout]
    A1 --> SAVE[Save to JSON]
    A3 --> OOP[Use Account object]
    A4 --> OOP
    A5 --> OOP
    OOP --> RCPT[print_receipt]
    RCPT --> SAVE
    SAVE --> MM
    A7 --> MAIN[Back to Main Menu]
```

## 4. Create account (type choice)

```mermaid
flowchart TD
    S[Select account type] --> T1[1 Savings]
    S --> T2[2 Checking]
    S --> T3[3 Back]
    T1 --> BAL[Opening balance + interest rate]
    T2 --> BAL2[Opening balance + overdraft limit]
    BAL --> ADD[Add account to customer list]
    BAL2 --> ADD
    ADD --> TX[Log OPENING transaction]
    TX --> RCP[Print receipt]
```

## 5. Deposit / withdraw (polymorphism)

```mermaid
flowchart TD
    P[Pick account number] --> BUILD[Build SavingsAccount or CheckingAccount]
    BUILD --> AMT[Enter amount]
    AMT --> VAL{Valid number?}
    VAL -->|No| ERR[Show error - try again]
    VAL -->|Yes| ACT{Deposit or Withdraw?}
    ACT -->|Deposit| DEP[account.deposit]
    ACT -->|Withdraw| WDR[account.withdraw]
    WDR --> RULE{Savings: min $100? Checking: overdraft?}
    RULE -->|Fail| DENY[Denied message]
    RULE -->|OK| UPD[Update balance in JSON]
    DEP --> UPD
    UPD --> RCP[print_receipt]
```

## 6. Transfer

```mermaid
flowchart TD
    T[Transfer] --> SRC[Source account]
    SRC --> DST[Destination account]
    DST --> AMT[Amount]
    AMT --> W[src_obj.withdraw]
    W --> OK{Success?}
    OK -->|No| STOP[Stop - no deposit]
    OK -->|Yes| D[dst_obj.deposit]
    D --> SAVE[Save both balances + 2 transaction rows]
    SAVE --> R1[Receipt source]
    R1 --> R2[Receipt destination]
```

## 7. Admin path (short)

```mermaid
flowchart LR
    A[Admin login] --> M[Admin Dashboard]
    M --> CRUD[Add / Update / Delete customers]
    M --> ACC[Add account for any customer]
    M --> VIEW[View customers, accounts, transactions]
    M --> OUT[Logout]
    OUT --> MAIN[Main Menu]
```
