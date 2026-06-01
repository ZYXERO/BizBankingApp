import json
import os
from datetime import datetime

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "bruhImTheAdmin"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "bizbanking_data.json")
LOG_FILE = os.path.join(BASE_DIR, "bizbanking_register.log")


class DataStore:
    def __init__(self):
        self.customers = []
        self.transactions = []
        self.next_id = 1

    def load(self):
        if not os.path.exists(DATA_FILE):
            self.seed()
            return
        try:
            with open(DATA_FILE, encoding="utf-8") as file:
                data = json.load(file)
            self.customers = data.get("customers", [])
            self.transactions = data.get("transactions", [])
            self.next_id = data.get("next_customer_id", 1)
            if self.customers:
                self.next_id = max(self.next_id, max(c["id"] for c in self.customers) + 1)
            self._fix_accounts()
            if not self.customers:
                self.seed()
        except (OSError, json.JSONDecodeError, TypeError, KeyError):
            print("\nCould not read saved data. Starting fresh.\n")
            self.customers = []
            self.transactions = []
            self.next_id = 1
            self.seed()

    def save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "next_customer_id": self.next_id,
                        "customers": self.customers,
                        "transactions": self.transactions,
                    },
                    file,
                    indent=2,
                )
        except OSError:
            print("\nCould not save data.\n")

    def new_id(self):
        value = self.next_id
        self.next_id += 1
        return value

    def by_username(self, username):
        for customer in self.customers:
            if customer["username"] == username:
                return customer
        return None

    def by_id(self, customer_id):
        for customer in self.customers:
            if customer["id"] == customer_id:
                return customer
        return None

    def new_account_number(self):
        return f"ACC{len(self.customers):04d}{len(self.transactions):04d}"

    def log_register(self, customer):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{stamp} | REGISTERED | id={customer['id']} | user={customer['username']}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(line)

    def _fix_accounts(self):
        for customer in self.customers:
            for account in customer.get("accounts", []):
                account.setdefault("type", "checking")
                account.setdefault("overdraft_limit", 0.0)
                account.setdefault("interest_rate", 0.02)

    def seed(self):
        if self.customers:
            return
        ayaan = {"id": self.new_id(), "name": "Ayaan Khan", "username": "ayaan", "password": "ayaan123", "accounts": []}
        sara = {"id": self.new_id(), "name": "Sara Ali", "username": "sara", "password": "sara123", "accounts": []}
        self.customers = [ayaan, sara]

        acc1 = {"type": "checking", "number": self.new_account_number(), "balance": 250.0, "overdraft_limit": 200.0}
        acc2 = {"type": "savings", "number": self.new_account_number(), "balance": 500.0, "interest_rate": 0.02}
        ayaan["accounts"].append(acc1)
        sara["accounts"].append(acc2)
        self.transactions = [
            {"account_number": acc1["number"], "customer_id": ayaan["id"], "type": "OPENING", "amount": 250.0, "description": "Seed"},
            {"account_number": acc2["number"], "customer_id": sara["id"], "type": "OPENING", "amount": 500.0, "description": "Seed"},
        ]
        self.save()
