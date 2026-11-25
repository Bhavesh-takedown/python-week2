"""
main.py
-------
Entry point -- demonstrates the OOP bank account system,
then triggers the pandas CSV analysis.
"""

from bank_account import BankAccount, SavingsAccount, CheckingAccount, InsufficientFundsError
import generate_data
import analysis


def demo_oop() -> None:
    print("\n" + "=" * 60)
    print("   PyBank -- OOP Demonstration")
    print("=" * 60)

    # -- Savings Account --------------------------------------------------
    print("\n[Savings Account -- Priya Sharma]")
    savings = SavingsAccount("Priya Sharma", initial_balance=10_000, interest_rate=0.06)
    savings.deposit(5_000, "salary")
    savings.deposit(2_500, "freelance payment")
    savings.withdraw(1_200, "grocery shopping")
    savings.apply_interest()
    savings.withdraw(3_000, "rent")
    savings.print_statement()

    # -- Checking Account -------------------------------------------------
    print("\n[Checking Account -- Rohan Mehta]")
    checking = CheckingAccount(
        "Rohan Mehta", initial_balance=2_000,
        overdraft_limit=1_000, transaction_fee=10
    )
    checking.deposit(8_000, "project payment")
    checking.withdraw(500,  "ATM withdrawal")
    checking.withdraw(2_000, "online shopping")

    # Test overdraft
    try:
        checking.withdraw(12_000, "huge purchase")
    except InsufficientFundsError as e:
        print(f"  [!] InsufficientFundsError: {e}")

    checking.print_statement()

    # -- Polymorphism demo ------------------------------------------------
    print("\n[Polymorphism -- iterating different account types]")
    accounts: list[BankAccount] = [savings, checking]
    for acc in accounts:
        print(f"  {acc}")

    # -- Class-level info -------------------------------------------------
    print(f"\n  Bank: {BankAccount.bank_name}")
    print(f"  Accounts created so far: {BankAccount._account_counter - 1000}")


def demo_pandas() -> None:
    print("\n\n" + "=" * 60)
    print("   Pandas CSV Analysis")
    print("=" * 60)

    print("\nGenerating synthetic dataset ...")
    rows = generate_data.generate_transactions(200)
    generate_data.save_csv(rows)

    print("\nRunning analysis ...")
    analysis.main()


if __name__ == "__main__":
    demo_oop()
    demo_pandas()
