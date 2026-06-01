# Draw.io guide + BizBanking flow (step by step)

## Part A — Open and edit the diagram in draw.io

### 1. Go to draw.io

1. Open a browser and go to [https://app.diagrams.net/](https://app.diagrams.net/).
2. If asked where to save, choose **Device** (files stay on your PC).

### 2. Open the project file

**Option A — Device (recommended)**

1. **File → Open from → Device**
2. Go to your project folder:
   ```
   BankingApp\docs\diagrams\bizbanking-thought-flow.drawio
   ```
3. Select the file and open it.

**Option B — Drag and drop**

1. In File Explorer, open `docs\diagrams\`.
2. Drag `bizbanking-thought-flow.drawio` onto the draw.io canvas.

**Option C — From GitHub (after you push)**

1. **File → Open from → GitHub**
2. Authorize draw.io once if prompted.
3. Pick repo `BizBankingApp` → branch `main` → `docs/diagrams/bizbanking-thought-flow.drawio`.

### 3. Edit the chart

| Task | How |
|------|-----|
| Move a box | Click it and drag |
| Change text | Double-click the shape |
| Add a shape | Drag from left **General** panel onto canvas |
| Connect two shapes | Hover a shape → blue arrows → drag to another shape |
| Delete | Select shape → **Delete** key |
| Undo | **Ctrl+Z** |

### 4. Save back to the project

1. **File → Save as…** (or **Ctrl+Shift+S**)
2. Save to the same path:
   ```
   docs\diagrams\bizbanking-thought-flow.drawio
   ```
3. In Cursor you should see the file update; commit when ready:
   ```powershell
   git add docs/diagrams/bizbanking-thought-flow.drawio
   git commit -m "Update thought-flow diagram"
   git push origin main
   ```

### 5. Export for slides or README image

1. **File → Export as → PNG** (or **SVG**)
2. Choose zoom **100%** or **200%** for sharper PNG
3. Save as e.g. `docs/diagrams/bizbanking-thought-flow.png`
4. In markdown you can link it: `![Flow](diagrams/bizbanking-thought-flow.png)`

---

## Part B — Application flow (what the diagram means)

This is the same logic as the `.drawio` file and [THOUGHT-FLOW.md](THOUGHT-FLOW.md).

### Step 1 — Start

| Step | What happens |
|------|----------------|
| 1 | Run `python main.py` from the project folder |
| 2 | App loads `data/bizbanking_data.json` |
| 3 | If the file is missing or empty → seed users **ayaan** / **sara** |
| 4 | Show **Welcome to BizBanking** |

### Step 2 — Welcome menu (loop until exit)

| Choice | Input examples | Result |
|--------|----------------|--------|
| **Login** | `1`, `login` | Ask username → password |
| **Register** | `2`, `register` | New customer → save JSON + log → back to welcome |
| **Exit** | `3`, `exit`, `quit`, **Esc** | App ends |

Invalid input → short error → menu again (menu text not repeated every time).

### Step 3 — After login

| User | Credentials (demo) | Next screen |
|------|-------------------|-------------|
| **Admin** | `admin` / `bruhImTheAdmin` | Admin dashboard (manage customers) |
| **Customer** | e.g. `sara` / `sara123` | Master menu (your accounts) |
| **Wrong** | — | Message → back to welcome |

**Esc** during username/password on Windows → back to welcome.

### Step 4 — Customer master menu (loop until logout)

| # | Action | Brief flow |
|---|--------|------------|
| 1 | Create account | Pick savings or checking → opening balance → save → receipt |
| 2 | View accounts | List account numbers, types, balances |
| 3 | Deposit | Pick account → amount → `deposit()` on model → save → receipt |
| 4 | Withdraw | Pick account → amount → `withdraw()` (savings min $100 / checking overdraft) → save → receipt |
| 5 | Transfer | Source account → destination → amount → withdraw then deposit → save → receipts |
| 6 | Close account | Pick account → remove from customer → save |
| 7 | Logout | Return to welcome menu |

### Step 5 — Where OOP fits (deposit / withdraw / transfer)

```
JSON dict (account row)
    → build SavingsAccount or CheckingAccount
    → call deposit() or withdraw()  ← rules differ by type
    → write new balance back to dict
    → append transaction row
    → save JSON
    → print_receipt()
```

### Step 6 — Admin (optional path)

1. Login as admin  
2. Add / update / delete customers, add accounts, view data  
3. Logout → welcome menu  

### Step 7 — End

- Choose **Exit** on welcome, or close the terminal.

---

## Part C — Quick test path (demo in class)

1. `python main.py`  
2. Login: `sara` / `sara123`  
3. **2** — view accounts  
4. **3** — deposit on an account → see receipt  
5. **4** — withdraw from savings → see $100 minimum rule if balance would go below $100  
6. **7** — logout  
7. **3** — exit  

---

## Which doc to use when

| Need | Use |
|------|-----|
| Edit visual diagram | This guide + `.drawio` file |
| View flow in GitHub (no draw.io) | [THOUGHT-FLOW.md](THOUGHT-FLOW.md) |
| Classes and files | [ARCHITECTURE.md](ARCHITECTURE.md) |
| JSON vs objects | [DATA-FLOW.md](DATA-FLOW.md) |
| Assignment steps 1–13 | [PHASE-GUIDE.md](PHASE-GUIDE.md) |
