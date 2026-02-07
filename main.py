from pathlib import Path
import json
import random
import string
from typing import List, Dict, Optional

# -------------------- DATABASE --------------------

DB_PATH = Path("data.json")


def load_data() -> List[Dict]:
    return json.loads(DB_PATH.read_text())


def save_data(data: List[Dict]) -> None:
    DB_PATH.write_text(json.dumps(data, indent=4))


# -------------------- BANK LOGIC --------------------

class Bank:
    def __init__(self):
        self.data = load_data()

    # ---------- Helpers ----------

    @staticmethod
    def _generate_account_number() -> str:
        letters = random.choices(string.ascii_uppercase, k=4)
        digits = random.choices(string.digits, k=8)
        acc = letters + digits
        random.shuffle(acc)
        return "".join(acc)

    def _find_user(self, account_no: str, pin: int) -> Optional[Dict]:
        for user in self.data:
            if user["account_no"] == account_no and user["pin"] == pin:
                return user
        return None

    # ---------- Core Operations ----------

    def create_account(
        self,
        name: str,
        email: str,
        age: int,
        phone: str,
        pin: int
    ) -> Dict:

        if age < 18:
            return {"success": False, "message": "User must be at least 18 years old"}

        if len(phone) != 10 or not phone.isdigit():
            return {"success": False, "message": "Phone number must be 10 digits"}

        if len(str(pin)) != 4:
            return {"success": False, "message": "PIN must be exactly 4 digits"}

        account = {
            "name": name,
            "email": email,
            "age": age,
            "phone": phone,
            "pin": pin,
            "account_no": self._generate_account_number(),
            "balance": 0
        }

        self.data.append(account)
        save_data(self.data)

        return {
            "success": True,
            "account_no": account["account_no"]
        }

    def deposit(self, account_no: str, pin: int, amount: int) -> Dict:
        user = self._find_user(account_no, pin)
        if not user:
            return {"success": False, "message": "Invalid credentials"}

        if amount <= 0 or amount > 100000:
            return {"success": False, "message": "Deposit must be between 1 and 10000"}

        user["balance"] += amount
        save_data(self.data)

        return {
            "success": True,
            "balance": user["balance"]
        }

    def withdraw(self, account_no: str, pin: int, amount: int) -> Dict:
        user = self._find_user(account_no, pin)
        if not user:
            return {"success": False, "message": "Invalid credentials"}

        if amount <= 0 or amount > 10000:
            return {"success": False, "message": "Withdrawal must be between 1 and 10000"}

        if user["balance"] < amount:
            return {"success": False, "message": "Insufficient balance"}

        user["balance"] -= amount
        save_data(self.data)

        return {
            "success": True,
            "balance": user["balance"]
        }

    def get_account_details(self, account_no: str, pin: int) -> Dict:
        user = self._find_user(account_no, pin)
        if not user:
            return {"success": False, "message": "Invalid credentials"}

        return {
            "success": True,
            "data": {
                "name": user["name"],
                "email": user["email"],
                "age": user["age"],
                "phone": user["phone"],
                "account_no": user["account_no"],
                "balance": user["balance"]
            }
        }

    def delete_account(self, account_no: str, pin: int) -> Dict:
        user = self._find_user(account_no, pin)
        if not user:
            return {"success": False, "message": "Invalid credentials"}

        self.data.remove(user)
        save_data(self.data)

        return {
            "success": True,
            "message": "Account deleted successfully"
        }