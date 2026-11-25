"""
generate_data.py
----------------
Generates a realistic synthetic CSV dataset of bank transactions
that is then analysed in analysis.py using pandas.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

ACCOUNTS = [
    {"id": "ACC1001", "owner": "Priya Sharma",    "type": "Savings"},
    {"id": "ACC1002", "owner": "Rohan Mehta",     "type": "Checking"},
    {"id": "ACC1003", "owner": "Ananya Iyer",     "type": "Savings"},
    {"id": "ACC1004", "owner": "Vikram Nair",     "type": "Checking"},
    {"id": "ACC1005", "owner": "Sneha Kapoor",    "type": "Savings"},
]

TRANSACTION_TYPES = ["deposit", "withdrawal", "interest credit", "transaction fee"]
NOTES = [
    "salary", "groceries", "rent", "utility bill", "online shopping",
    "restaurant", "medical", "transfer", "ATM", "subscription",
    "", "", "",   # blank notes are common
]

START_DATE = datetime(2025, 1, 1)


def random_date(start: datetime, days: int = 365) -> str:
    delta = timedelta(days=random.randint(0, days))
    return (start + delta).strftime("%Y-%m-%d")


def generate_transactions(n: int = 200) -> list[dict]:
    rows = []
    for _ in range(n):
        acc = random.choice(ACCOUNTS)
        t_type = random.choice(TRANSACTION_TYPES)

        if t_type == "interest credit":
            amount = round(random.uniform(50, 500), 2)
        elif t_type == "transaction fee":
            amount = round(random.choice([5, 10, 15, 20]), 2)
        elif t_type == "withdrawal":
            amount = round(random.uniform(100, 8000), 2)
        else:
            amount = round(random.uniform(500, 50000), 2)

        rows.append({
            "date": random_date(START_DATE),
            "account_id": acc["id"],
            "owner": acc["owner"],
            "account_type": acc["type"],
            "transaction_type": t_type,
            "amount": amount,
            "note": random.choice(NOTES),
        })

    rows.sort(key=lambda r: r["date"])
    return rows


def save_csv(rows: list[dict], path: str = "transactions.csv") -> None:
    fieldnames = ["date", "account_id", "owner", "account_type",
                  "transaction_type", "amount", "note"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [+] Saved {len(rows)} rows -> {path}")


if __name__ == "__main__":
    rows = generate_transactions(200)
    save_csv(rows)
