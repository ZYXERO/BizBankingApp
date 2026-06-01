# Organize the GitHub repo (folders + commands)

Suggested layout for BizBanking:

```text
BizBankingApp/
├── README.md
├── LICENSE
├── .gitignore
├── main.py                 # run: python main.py
├── src/                    # all Python code
│   ├── app.py
│   ├── ui.py
│   ├── storage.py
│   └── models/
├── data/                   # JSON + runtime logs
│   ├── bizbanking_data.json
│   └── bizbanking_register.log
├── docs/                   # markdown + Mermaid
│   └── diagrams/           # .drawio (source)
└── visuals/                # optional: exported PNG/SVG from draw.io
```

`docs/` = written docs. `docs/diagrams/` = editable draw.io. `visuals/` = images for README/slides.

---

## Before you start

```powershell
cd c:\Users\kaush\Desktop\github\Collabera_Training\BankingApp
git status
```

Commit or stash anything uncommitted. Use **`git mv`** (not plain `move`) so GitHub keeps file history.

---

## Step 1 — Create folders

```powershell
New-Item -ItemType Directory -Force -Path src, data, visuals
```

---

## Step 2 — Move files (git mv)

```powershell
git mv app.py src/
git mv ui.py src/
git mv storage.py src/
git mv models src/
git mv bizbanking_data.json data/
```

If `bizbanking_register.log` is tracked:

```powershell
git mv bizbanking_register.log data/
```

Optional: export PNG from draw.io into `visuals/`, then:

```powershell
git add visuals/bizbanking-thought-flow.png
```

Remove old entry point if you replace it:

```powershell
git rm Main.py
```

---

## Step 3 — Fix `storage.py` paths

In `src/storage.py`, point at the `data/` folder (project root = parent of `src/`):

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "bizbanking_data.json"
LOG_FILE = PROJECT_ROOT / "data" / "bizbanking_register.log"
```

Use `str(DATA_FILE)` where you pass paths to `open()` / `os.path.exists()`.

---

## Step 4 — Root `main.py` (entry point)

Create **`main.py`** at repo root (not inside `src/`):

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from app import BizBankingApp


def run():
    app = BizBankingApp()
    app.db.load()
    app.run()


if __name__ == "__main__":
    run()
```

Run from project root:

```powershell
python main.py
```

Imports inside `src/` stay the same (`from models...`, `from storage...`, `import ui`).

---

## Step 5 — Update README

Change run instructions from `python Main.py` to:

```text
python main.py
```

Mention that `data/bizbanking_data.json` must be copied with the project.

---

## Step 6 — Commit and push

```powershell
git add main.py docs/REPO-ORGANIZE.md
git status
git commit -m "Reorganize repo into src, data, and docs folders"
git push origin main
```

---

## One-shot script (copy/paste)

Run only after you understand the steps above. It moves files but **does not** edit `storage.py` or create `main.py` for you.

```powershell
cd c:\Users\kaush\Desktop\github\Collabera_Training\BankingApp

New-Item -ItemType Directory -Force -Path src, data, visuals | Out-Null

git mv app.py src/
git mv ui.py src/
git mv storage.py src/
git mv models src/
git mv bizbanking_data.json data/

if (Test-Path bizbanking_register.log) { git mv bizbanking_register.log data/ }
if (Test-Path Main.py) { git rm Main.py }

Write-Host "Done moving. Next: edit src/storage.py, add root main.py, test python main.py"
```

---

## `.gitignore` tips

Your template ignores `*.log`. That is fine for `data/bizbanking_register.log` (local only). Keep **`data/bizbanking_data.json`** tracked so demo users travel with the repo.

Optional add to `.gitignore`:

```gitignore
# local overrides
data/*.log
visuals/*.tmp
```

---

## Do not move (keep at root)

| Item | Why |
|------|-----|
| `README.md` | GitHub home page |
| `LICENSE` | Standard location |
| `.gitignore` | Repo root |
| `main.py` | Obvious entry command |

---

## If something breaks after the move

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: models` | Run `python main.py` from repo root; check `sys.path` in `main.py` |
| Empty / new data file | Copy old JSON into `data/` or let app seed again |
| `Main.py` still referenced | Use `python main.py` only |

---

## Lighter option (data only)

If you only want tidier data files without moving Python:

```powershell
New-Item -ItemType Directory -Force -Path data
git mv bizbanking_data.json data/
git mv bizbanking_register.log data/
```

Then only update paths in `storage.py` as in Step 3.
