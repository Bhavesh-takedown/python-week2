"""
analysis.py
-----------
Pandas-powered analysis of the bank transaction CSV dataset.

Produces:
  1. Summary statistics per account
  2. Monthly transaction volume
  3. Top depositors
  4. Withdrawal vs deposit ratio
  5. Saves all summary tables to analysis_report.csv
"""

import pandas as pd
import sys
from pathlib import Path

CSV_FILE = Path("transactions.csv")


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------

def banner(title: str) -> None:
    width = 60
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}")


def load_data(path: Path = CSV_FILE) -> pd.DataFrame:
    if not path.exists():
        sys.exit(
            f"[ERROR] '{path}' not found.\n"
            "Run:  python generate_data.py   first."
        )
    df = pd.read_csv(path, parse_dates=["date"])
    print(f"\n[+] Loaded {len(df):,} transactions from '{path}'")
    return df


# ──────────────────────────────────────────────────────────────────────
# analysis functions
# ──────────────────────────────────────────────────────────────────────

def overview(df: pd.DataFrame) -> None:
    banner("1 · Dataset Overview")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))
    print("\nBasic statistics (amount):")
    print(df["amount"].describe().round(2).to_string())


def per_account_summary(df: pd.DataFrame) -> pd.DataFrame:
    banner("2 · Per-Account Summary")
    summary = (
        df.groupby(["account_id", "owner", "account_type"])["amount"]
        .agg(
            total_transactions="count",
            total_amount="sum",
            avg_amount="mean",
            max_amount="max",
            min_amount="min",
        )
        .reset_index()
        .sort_values("total_amount", ascending=False)
    )
    summary[["total_amount", "avg_amount", "max_amount", "min_amount"]] = (
        summary[["total_amount", "avg_amount", "max_amount", "min_amount"]].round(2)
    )
    print(summary.to_string(index=False))
    return summary


def monthly_volume(df: pd.DataFrame) -> pd.DataFrame:
    banner("3 · Monthly Transaction Volume")
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")
    monthly = (
        df.groupby("month")["amount"]
        .agg(count="count", total="sum")
        .reset_index()
    )
    monthly["total"] = monthly["total"].round(2)
    print(monthly.to_string(index=False))
    return monthly


def top_depositors(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    banner(f"4 · Top {top_n} Depositors (by total deposit amount)")
    deposits = df[df["transaction_type"] == "deposit"]
    top = (
        deposits.groupby(["owner", "account_type"])["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_deposited"})
        .sort_values("total_deposited", ascending=False)
        .head(top_n)
    )
    top["total_deposited"] = top["total_deposited"].round(2)
    print(top.to_string(index=False))
    return top


def deposit_vs_withdrawal(df: pd.DataFrame) -> pd.DataFrame:
    banner("5 · Deposit vs Withdrawal Ratio per Account")
    pivot = df[df["transaction_type"].isin(["deposit", "withdrawal"])].copy()
    ratio = (
        pivot.groupby(["account_id", "owner", "transaction_type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )
    if "deposit" in ratio.columns and "withdrawal" in ratio.columns:
        ratio["ratio (dep/with)"] = (ratio["deposit"] / ratio["withdrawal"]).round(2)
    ratio = ratio.round(2)
    print(ratio.to_string(index=False))
    return ratio


def transaction_type_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    banner("6 · Transaction Type Breakdown")
    breakdown = (
        df.groupby("transaction_type")["amount"]
        .agg(count="count", total="sum", avg="mean")
        .reset_index()
        .sort_values("total", ascending=False)
    )
    breakdown[["total", "avg"]] = breakdown[["total", "avg"]].round(2)
    print(breakdown.to_string(index=False))
    return breakdown


def save_report(frames: dict[str, pd.DataFrame], path: str = "analysis_report.csv") -> None:
    banner("Saving Report")
    with open(path, "w", newline="", encoding="utf-8") as f:
        for section, frame in frames.items():
            f.write(f"### {section} ###\n")
            frame.to_csv(f, index=False)
            f.write("\n")
    print(f"[+] Report saved -> {path}")


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------

def main() -> None:
    df = load_data()

    overview(df)
    acc_summary  = per_account_summary(df)
    monthly      = monthly_volume(df)
    depositors   = top_depositors(df)
    ratio        = deposit_vs_withdrawal(df)
    breakdown    = transaction_type_breakdown(df)

    save_report({
        "Per-Account Summary":       acc_summary,
        "Monthly Volume":            monthly,
        "Top Depositors":            depositors,
        "Deposit vs Withdrawal":     ratio,
        "Transaction Type Breakdown": breakdown,
    })


if __name__ == "__main__":
    main()
