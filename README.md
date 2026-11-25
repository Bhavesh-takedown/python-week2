# 02 · OOP Bank Account 🏦

> **Python + pandas** — Week 2 project  
> OOP banking system with transaction history, paired with a CSV dataset analysis using pandas.

---

## 📁 Project Structure

```
pythonweek2/
├── bank_account.py     # Core OOP classes
├── generate_data.py    # Synthetic CSV data generator
├── analysis.py         # Pandas-powered analysis
├── main.py             # Entry point (runs everything)
├── requirements.txt
└── .gitignore
```

---

## 🧱 OOP Design

### `BankAccount` (base class)
| Feature | Detail |
|---|---|
| Attributes | `owner`, `balance`, `account_number` |
| Methods | `deposit()`, `withdraw()`, `get_balance()`, `print_statement()` |
| Transaction log | Every operation is recorded with timestamp & note |

### `SavingsAccount` ← extends `BankAccount`
- Configurable annual interest rate (default **4% p.a.**)
- `apply_interest()` credits interest and logs it

### `CheckingAccount` ← extends `BankAccount`
- Overdraft facility (default limit ₹500)
- Flat transaction fee per withdrawal (default ₹5)
- Overrides `withdraw()` to deduct fee automatically

### Custom Exception
- `InsufficientFundsError` — raised when a withdrawal exceeds available funds + overdraft

---

## 📊 Pandas Analysis

The `generate_data.py` script creates **200 synthetic transactions** across 5 accounts and saves them to `transactions.csv`.  
`analysis.py` then produces six analysis sections:

| # | Section |
|---|---|
| 1 | Dataset overview & basic stats |
| 2 | Per-account summary (total, avg, max, min) |
| 3 | Monthly transaction volume |
| 4 | Top depositors by total amount |
| 5 | Deposit vs withdrawal ratio |
| 6 | Transaction type breakdown |

Results are also saved to **`analysis_report.csv`**.

---

## 🚀 How to Run

```bash
# 1. Install dependency
pip install -r requirements.txt

# 2. Run everything (OOP demo + pandas analysis)
python main.py

# Or run individually:
python generate_data.py   # generates transactions.csv
python analysis.py        # analyses the CSV
```

---

## 💡 Concepts Demonstrated

- **Encapsulation** — private `_balance` and `_transactions` attributes
- **Inheritance** — `SavingsAccount` and `CheckingAccount` extend `BankAccount`
- **Polymorphism** — `withdraw()` behaves differently per subclass
- **Custom Exceptions** — `InsufficientFundsError`
- **pandas** — `groupby`, `pivot`, `agg`, `describe`, `to_period`, CSV I/O
