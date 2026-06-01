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
