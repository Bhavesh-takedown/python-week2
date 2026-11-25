"""
OOP Bank Account System
-----------------------
Demonstrates Object-Oriented Programming with:
  - BankAccount base class
  - SavingsAccount and CheckingAccount subclasses
  - Full transaction history tracking
"""

from datetime import datetime


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
    pass


class BankAccount:
    """Base class representing a generic bank account."""

    bank_name = "PyBank"
    _account_counter = 1000

    def __init__(self, owner: str, initial_balance: float = 0.0):
        """
        Initialise a new BankAccount.

        Args:
            owner: Full name of the account holder.
            initial_balance: Starting balance (must be >= 0).
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        BankAccount._account_counter += 1
        self._account_number = BankAccount._account_counter
        self._owner = owner
        self._balance = initial_balance
        self._transactions: list[dict] = []

        if initial_balance > 0:
            self._log_transaction("initial deposit", initial_balance)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _log_transaction(self, t_type: str, amount: float, note: str = "") -> dict:
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": t_type,
            "amount": round(amount, 2),
            "balance_after": round(self._balance, 2),
            "note": note,
        }
        self._transactions.append(record)
        return record

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def deposit(self, amount: float, note: str = "") -> None:
        """Deposit a positive amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._log_transaction("deposit", amount, note)
        print(f"  [+] Deposited Rs.{amount:,.2f}. New balance: Rs.{self._balance:,.2f}")

    def withdraw(self, amount: float, note: str = "") -> None:
        """Withdraw an amount from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw Rs.{amount:,.2f}. "
                f"Available balance: Rs.{self._balance:,.2f}"
            )
        self._balance -= amount
        self._log_transaction("withdrawal", amount, note)
        print(f"  [-] Withdrew Rs.{amount:,.2f}. New balance: Rs.{self._balance:,.2f}")

    def get_balance(self) -> float:
        """Return the current balance."""
        return round(self._balance, 2)

    def get_transaction_history(self) -> list[dict]:
        """Return a copy of the transaction history."""
        return list(self._transactions)

    def print_statement(self) -> None:
        """Pretty-print the account statement."""
        print(f"\n{'='*60}")
        print(f"  {self.bank_name} -- Account Statement")
        print(f"  Account #: {self._account_number}  |  Owner: {self._owner}")
        print(f"  Type: {self.__class__.__name__}")
        print(f"{'='*60}")
        print(f"  {'Date & Time':<22} {'Type':<18} {'Amount':>12} {'Balance':>12}")
        print(f"  {'-'*66}")
        for t in self._transactions:
            note_str = f"  [{t['note']}]" if t['note'] else ""
            print(
                f"  {t['timestamp']:<22} {t['type']:<18} "
                f"Rs.{t['amount']:>9,.2f} Rs.{t['balance_after']:>9,.2f}"
                + note_str
            )
        print(f"{'='*60}")
        print(f"  Current Balance: Rs.{self._balance:,.2f}")
        print(f"{'='*60}\n")

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(#{self._account_number}, "
            f"owner='{self._owner}', balance=Rs.{self._balance:,.2f})"
        )

    def __repr__(self) -> str:
        return self.__str__()


# ======================================================================
# Sub-classes
# ======================================================================

class SavingsAccount(BankAccount):
    """
    A savings account that earns interest.

    Attributes:
        interest_rate: Annual interest rate as a decimal (e.g. 0.05 = 5%).
    """

    DEFAULT_RATE = 0.04  # 4% per annum

    def __init__(self, owner: str, initial_balance: float = 0.0,
                 interest_rate: float = DEFAULT_RATE):
        super().__init__(owner, initial_balance)
        if not (0 <= interest_rate <= 1):
            raise ValueError("Interest rate must be between 0 and 1.")
        self.interest_rate = interest_rate

    def apply_interest(self) -> float:
        """Apply annual interest to the balance and return the interest earned."""
        interest = round(self._balance * self.interest_rate, 2)
        self._balance += interest
        self._log_transaction(
            "interest credit", interest,
            f"{self.interest_rate * 100:.1f}% p.a."
        )
        print(f"  [*] Interest of Rs.{interest:,.2f} credited. "
              f"New balance: Rs.{self._balance:,.2f}")
        return interest


class CheckingAccount(BankAccount):
    """
    A checking account with an overdraft facility.

    Attributes:
        overdraft_limit: Maximum amount the account can go into negative.
        transaction_fee: Flat fee charged on every withdrawal.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0,
                 overdraft_limit: float = 500.0, transaction_fee: float = 5.0):
        super().__init__(owner, initial_balance)
        self.overdraft_limit = abs(overdraft_limit)
        self.transaction_fee = abs(transaction_fee)

    def withdraw(self, amount: float, note: str = "") -> None:
        """Withdraw with overdraft support and a per-transaction fee."""
        total_deduction = amount + self.transaction_fee
        if total_deduction > self._balance + self.overdraft_limit:
            raise InsufficientFundsError(
                f"Exceeds overdraft limit. Available: "
                f"Rs.{self._balance + self.overdraft_limit:,.2f}"
            )
        self._balance -= total_deduction
        self._log_transaction("withdrawal", amount, note)
        self._log_transaction("transaction fee", self.transaction_fee)
        print(
            f"  [-] Withdrew Rs.{amount:,.2f} (fee: Rs.{self.transaction_fee:,.2f}). "
            f"New balance: Rs.{self._balance:,.2f}"
        )
