from decimal import Decimal, InvalidOperation

from models.checking_account import CheckingAccount
from models.customer import Customer
from models.savings_account import SavingsAccount
from storage import ADMIN_PASSWORD, ADMIN_USERNAME, DataStore
import ui

MAIN_MENU = {"login": {"1", "login"}, "register": {"2", "register"}, "exit": {"3", "exit", "quit", "q"}}
MASTER_MENU = {
    "create": {"1", "create", "open", "new", "account", "accounts"},
    "view": {"2", "view", "all", "account", "accounts"},
    "deposit": {"3", "deposit", "add"},
    "withdraw": {"4", "withdraw", "take"},
    "transfer": {"5", "transfer", "send", "move"},
    "close": {"6", "close", "delete", "remove", "account", "accounts"},
    "logout": {"7", "logout", "log", "out", "exit", "back"},
}
TYPE_MENU = {"savings": {"1", "savings", "save"}, "checking": {"2", "checking", "check"}, "back": {"3", "back", "exit", "quit", "q"}}
ADMIN_MENU = {
    "add_customer": {"1", "add", "customer", "customers", "new"},
    "update_customer": {"2", "update", "edit", "customer", "customers"},
    "add_account": {"3", "account", "accounts", "open"},
    "delete_customer": {"4", "delete", "remove", "customer", "customers"},
    "view_customers": {"5", "view", "list", "customer", "customers"},
    "view_accounts": {"6", "view", "all", "account", "accounts"},
    "view_transactions": {"7", "view", "all", "transaction", "transactions"},
    "logout": {"8", "logout", "log", "out"},
}


class BizBankingApp:
    def __init__(self):
        self.db = DataStore()

    def run_block(self, title, action):
        ui.section(title)
        try:
            action()
        except Exception as exc:
            print(f"\nError: {exc}\n")
        finally:
            ui.section_end()

    def menu_loop(self, title, welcome, options, token_map, handlers):
        ui.show_menu(title, welcome, options)
        while True:
            choice = ui.read_line("Enter your choice: ", allow_escape=False)
            action = ui.parse_menu(choice, token_map)
            if action is None:
                print("\nInvalid choice.\n")
                continue
            if action == "logout":
                handlers["logout"]()
                return
            try:
                handlers[action]()
            except Exception as exc:
                print(f"\nError: {exc}\n")

    def read_money(self, prompt, positive=False):
        raw = ui.read_line(prompt, allow_escape=False)
        if raw is None:
            return None
        try:
            value = Decimal(raw.strip())
        except (InvalidOperation, ValueError):
            print("\nPlease enter a valid number.\n")
            return None
        if value < 0:
            print("\nAmount cannot be negative.\n")
            return None
        if positive and value <= 0:
            print("\nAmount must be greater than zero.\n")
            return None
        return value

    def read_int(self, prompt):
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("\nPlease enter a whole number.\n")
            return None

    def credentials(self):
        username = ui.read_line("Please enter your username: ")
        if username is None or not username:
            return None, None
        password = ui.read_line("Please enter your password: ")
        print()
        if password is None or not password:
            return None, None
        return username, password

    def to_customer(self, data):
        parts = data["name"].split()
        first = parts[0]
        last = " ".join(parts[1:]) if len(parts) > 1 else ""
        return Customer(data["id"], first, last)

    def to_account(self, customer_data, account_data):
        holder = self.to_customer(customer_data)
        balance = Decimal(str(account_data.get("balance", 0)))
        if account_data.get("type") == "savings":
            rate = Decimal(str(account_data.get("interest_rate", 0.02)))
            return SavingsAccount(account_data["number"], holder, balance, rate)
        limit = Decimal(str(account_data.get("overdraft_limit", 0)))
        return CheckingAccount(account_data["number"], holder, balance, limit)

    def find_account(self, customer, number):
        for account in customer.get("accounts", []):
            if account["number"] == number:
                return account
        return None

    def find_account_any(self, number):
        for customer in self.db.customers:
            account = self.find_account(customer, number)
            if account:
                return customer, account
        return None, None

    def print_accounts(self, customer):
        if not customer["accounts"]:
            print("No accounts found.")
            return
        for account in customer["accounts"]:
            kind = account.get("type", "checking").title()
            print(f"{kind} | {account['number']} | Balance: ${account['balance']:.2f}")

    def receipt(self, customer, account_data, tx_type, amount):
        obj = self.to_account(customer, account_data)
        obj._last_transaction_type = tx_type
        obj._last_transaction_amount = amount
        print()
        obj.print_receipt()
        print()

    def add_transaction(self, account_number, customer_id, tx_type, amount, description):
        self.db.transactions.append(
            {
                "account_number": account_number,
                "customer_id": customer_id,
                "type": tx_type,
                "amount": float(amount),
                "description": description,
            }
        )

    def login(self):
        print()
        username, password = self.credentials()
        if username is None:
            return
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("\nLogin successful!\n")
            self.admin_menu()
            return
        customer = self.db.by_username(username)
        if customer and customer["password"] == password:
            print("\nLogin successful!\n")
            self.master_menu(customer)
            return
        print("\nInvalid username or password.\n")

    def register(self):
        def work():
            print("Welcome! Let's create your new account.\n")
            name = ui.read_line("Enter your full name: ")
            print()
            if name is None or not name:
                return
            username, password = self.credentials()
            if username is None:
                return
            if username == ADMIN_USERNAME or self.db.by_username(username):
                print("\nUsername already exists.\n")
                return
            customer = {"id": self.db.new_id(), "name": name, "username": username, "password": password, "accounts": []}
            self.db.customers.append(customer)
            self.db.save()
            self.db.log_register(customer)
            print("\nRegistration successful!\n")

        self.run_block("Registration", work)

    def master_menu(self, customer):
        name = customer["name"]
        options = [
            "1. Create Account",
            "2. View All Accounts",
            "3. Deposit",
            "4. Withdraw",
            "5. Transfer",
            "6. Close Account",
            "7. Logout",
        ]

        def create():
            self.create_account(customer)

        def view():
            self.run_block("All Accounts", lambda: self.print_accounts(customer))

        self.menu_loop(
            "Master Menu",
            f"Welcome back, {name}!",
            options,
            MASTER_MENU,
            {
                "create": create,
                "view": view,
                "deposit": lambda: self.deposit(customer),
                "withdraw": lambda: self.withdraw(customer),
                "transfer": lambda: self.transfer(customer),
                "close": lambda: self.close_account(customer),
                "logout": lambda: print("\nLogged out successfully.\n"),
            },
        )

    def create_account(self, customer):
        def work():
            print("1. Savings Account\n2. Checking Account\n3. Back\n")
            choice = ui.parse_menu(ui.read_line("Enter your choice: "), TYPE_MENU)
            if choice in (None, "back"):
                return
            opening = self.read_money("Enter opening balance: ")
            if opening is None:
                return
            number = self.db.new_account_number()
            if choice == "savings":
                rate = self.read_money("Enter interest rate (example 0.02): ")
                if rate is None:
                    return
                account = {"type": "savings", "number": number, "balance": float(opening), "interest_rate": float(rate)}
            else:
                limit = self.read_money("Enter overdraft limit: ")
                if limit is None:
                    return
                account = {"type": "checking", "number": number, "balance": float(opening), "overdraft_limit": float(limit)}
            customer["accounts"].append(account)
            self.add_transaction(number, customer["id"], "OPENING", opening, "Account opened")
            self.db.save()
            print(f"\nAccount created: {number}\n")
            self.receipt(customer, account, "OPENING", opening)

        self.run_block("Create Account", work)

    def deposit(self, customer):
        def work():
            self.print_accounts(customer)
            if not customer["accounts"]:
                return
            number = ui.read_line("Enter account number: ")
            if number is None:
                return
            account = self.find_account(customer, number.strip())
            if not account:
                print("\nAccount not found.\n")
                return
            amount = self.read_money("Enter deposit amount: ", positive=True)
            if amount is None:
                return
            obj = self.to_account(customer, account)
            if not obj.deposit(amount):
                print("\nDeposit failed.\n")
                return
            account["balance"] = float(obj.balance)
            self.add_transaction(account["number"], customer["id"], "DEPOSIT", amount, "Deposit")
            self.db.save()
            self.receipt(customer, account, "DEPOSIT", amount)

        self.run_block("Deposit", work)

    def withdraw(self, customer):
        def work():
            self.print_accounts(customer)
            if not customer["accounts"]:
                return
            number = ui.read_line("Enter account number: ")
            if number is None:
                return
            account = self.find_account(customer, number.strip())
            if not account:
                print("\nAccount not found.\n")
                return
            amount = self.read_money("Enter withdraw amount: ", positive=True)
            if amount is None:
                return
            obj = self.to_account(customer, account)
            if not obj.withdraw(amount):
                print("\nWithdraw denied (rules or insufficient funds).\n")
                return
            account["balance"] = float(obj.balance)
            self.add_transaction(account["number"], customer["id"], "WITHDRAW", amount, "Withdraw")
            self.db.save()
            self.receipt(customer, account, "WITHDRAW", amount)

        self.run_block("Withdraw", work)

    def transfer(self, customer):
        def work():
            self.print_accounts(customer)
            if not customer["accounts"]:
                return
            src_no = ui.read_line("Enter source account number: ")
            if src_no is None:
                return
            src = self.find_account(customer, src_no.strip())
            if not src:
                print("\nSource account not found.\n")
                return
            dst_no = ui.read_line("Enter destination account number: ", allow_escape=False)
            dst_customer, dst = self.find_account_any(dst_no.strip())
            if not dst:
                print("\nDestination account not found.\n")
                return
            if dst["number"] == src["number"]:
                print("\nSource and destination must be different.\n")
                return
            amount = self.read_money("Enter transfer amount: ", positive=True)
            if amount is None:
                return
            src_obj = self.to_account(customer, src)
            if not src_obj.withdraw(amount):
                print("\nTransfer denied (rules or insufficient funds).\n")
                return
            dst_obj = self.to_account(dst_customer, dst)
            if not dst_obj.deposit(amount):
                print("\nTransfer failed.\n")
                return
            src["balance"] = float(src_obj.balance)
            dst["balance"] = float(dst_obj.balance)
            self.add_transaction(src["number"], customer["id"], "TRANSFER_OUT", amount, f"To {dst['number']}")
            self.add_transaction(dst["number"], dst_customer["id"], "TRANSFER_IN", amount, f"From {src['number']}")
            self.db.save()
            print("\nTransfer successful.\n")
            self.receipt(customer, src, "TRANSFER_OUT", amount)
            self.receipt(dst_customer, dst, "TRANSFER_IN", amount)

        self.run_block("Transfer", work)

    def close_account(self, customer):
        def work():
            self.print_accounts(customer)
            if not customer["accounts"]:
                return
            number = ui.read_line("Enter account number to close: ")
            if number is None:
                return
            account = self.find_account(customer, number.strip())
            if not account:
                print("\nAccount not found.\n")
                return
            if input(f"Close account {number}? (y/n): ").strip().lower() != "y":
                print("\nCancelled.\n")
                return
            customer["accounts"].remove(account)
            self.add_transaction(number.strip(), customer["id"], "CLOSE", Decimal("0"), "Account closed")
            self.db.save()
            print("\nAccount closed.\n")

        self.run_block("Close Account", work)

    def admin_menu(self):
        options = [
            "1. Add Customer",
            "2. Update Customer",
            "3. Add Account",
            "4. Delete Customer",
            "5. View Customers",
            "6. View All Accounts",
            "7. View All Transactions",
            "8. Logout",
        ]
        self.menu_loop(
            "Admin Dashboard",
            "Welcome back, Administrator!",
            options,
            ADMIN_MENU,
            {
                "add_customer": self.add_customer,
                "update_customer": self.update_customer,
                "add_account": self.add_account_admin,
                "delete_customer": self.delete_customer,
                "view_customers": self.view_customers,
                "view_accounts": self.view_all_accounts,
                "view_transactions": self.view_all_transactions,
                "logout": lambda: print("\nLogged out successfully.\n"),
            },
        )

    def add_customer(self):
        def work():
            name = input("Enter customer name: ").strip()
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if not name or not username or not password:
                print("\nAll fields are required.\n")
                return
            if username == ADMIN_USERNAME or self.db.by_username(username):
                print("\nUsername already exists.\n")
                return
            customer = {"id": self.db.new_id(), "name": name, "username": username, "password": password, "accounts": []}
            self.db.customers.append(customer)
            self.db.save()
            print(f"\nCustomer added (ID: {customer['id']}).\n")

        self.run_block("Add Customer", work)

    def update_customer(self):
        def work():
            self.print_customers()
            if not self.db.customers:
                return
            customer_id = self.read_int("Enter customer ID to update: ")
            if customer_id is None:
                return
            customer = self.db.by_id(customer_id)
            if not customer:
                print("\nCustomer not found.\n")
                return
            new_name = input(f"Name [{customer['name']}]: ").strip()
            new_username = input(f"Username [{customer['username']}]: ").strip()
            new_password = input("New password (blank to keep): ").strip()
            if new_name:
                customer["name"] = new_name
            if new_username and new_username != customer["username"]:
                if self.db.by_username(new_username):
                    print("\nUsername already exists.\n")
                    return
                customer["username"] = new_username
            if new_password:
                customer["password"] = new_password
            self.db.save()
            print("\nCustomer updated.\n")

        self.run_block("Update Customer", work)

    def add_account_admin(self):
        def work():
            self.print_customers()
            if not self.db.customers:
                return
            customer_id = self.read_int("Enter customer ID: ")
            if customer_id is None:
                return
            opening = self.read_money("Enter opening balance: ")
            if opening is None:
                return
            customer = self.db.by_id(customer_id)
            if not customer:
                print("\nCustomer not found.\n")
                return
            number = self.db.new_account_number()
            account = {"type": "checking", "number": number, "balance": float(opening), "overdraft_limit": 0.0}
            customer["accounts"].append(account)
            self.add_transaction(number, customer_id, "OPENING", opening, "Account opened")
            self.db.save()
            print(f"\nAccount {number} created.\n")
            self.receipt(customer, account, "OPENING", opening)

        self.run_block("Add Account", work)

    def delete_customer(self):
        def work():
            self.print_customers()
            if not self.db.customers:
                return
            customer_id = self.read_int("Enter customer ID to delete: ")
            if customer_id is None:
                return
            customer = self.db.by_id(customer_id)
            if not customer:
                print("\nCustomer not found.\n")
                return
            if input(f"Delete {customer['name']}? (y/n): ").strip().lower() != "y":
                print("\nCancelled.\n")
                return
            self.db.customers.remove(customer)
            self.db.save()
            print("\nCustomer deleted.\n")

        self.run_block("Delete Customer", work)

    def print_customers(self):
        if not self.db.customers:
            print("No customers found.")
            return
        for customer in self.db.customers:
            print(f"ID: {customer['id']} | {customer['name']} | {customer['username']} | Accounts: {len(customer['accounts'])}")

    def view_customers(self):
        self.run_block("Customers", self.print_customers)

    def view_all_accounts(self):
        def work():
            found = False
            for customer in self.db.customers:
                for account in customer["accounts"]:
                    found = True
                    print(f"{customer['name']} | {account['number']} | ${account['balance']:.2f}")
            if not found:
                print("No accounts found.")

        self.run_block("All Accounts", work)

    def view_all_transactions(self):
        def work():
            if not self.db.transactions:
                print("No transactions found.")
                return
            for row in self.db.transactions:
                print(
                    f"{row['account_number']} | {row['type']} | ${row['amount']:.2f} | {row['description']}"
                )

        self.run_block("All Transactions", work)

    def run(self):
        show_welcome = True
        show_options = True
        try:
            while True:
                if show_welcome:
                    print(f"\nWelcome to {ui.APP_NAME}!\n")
                    show_welcome = False
                if show_options:
                    print("Please login to continue!\n\n1. Login\n2. Register\n3. Exit\n")
                    show_options = False
                choice = ui.read_line("Enter your choice: ")
                action = ui.parse_menu(choice, MAIN_MENU, none_action="exit")
                if action == "exit":
                    print(f"\nThank you for using {ui.APP_NAME}. Goodbye!\n")
                    break
                if action == "login":
                    self.login()
                    show_options = True
                elif action == "register":
                    self.register()
                    show_options = True
                else:
                    print("\nInvalid choice.\n")
        except KeyboardInterrupt:
            print(f"\nThank you for using {ui.APP_NAME}. Goodbye!\n")
