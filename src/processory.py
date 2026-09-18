"""
Data Processing Module 
1. Validating required dataset columns.
2. Filtering records using two specific conditions (.loc).
3. Counting missing values in the 'tq' column without altering them.
4. Creating two new derived columns (a scaled number and a flag/category).
5. Sorting records in descending order.
6. Recording every change in an audit log list.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


def validate_columns(df: pd.DataFrame, required_columns: set) -> None:
    """Checks if the dataset contains all required columns."""
    missing_cols = required_columns - set(df.columns)
    if missing_cols:
        raise KeyError(f"Dataset missing required column(s): {sorted(list(missing_cols))}")


def compute_audit_step(
    step: str,
    operation: str,
    rule: str,
    df_before: pd.DataFrame,
    df_after: pd.DataFrame
) -> Dict[str, Any]:
    """Creates a single audit log entry tracking row counts before and after."""
    return {
        "step": step,
        "operation": operation,
        "rule": rule,
        "rows_before": len(df_before),
        "rows_after": len(df_after)
    }


class DataProcessor:
    """Main processor class that cleans, filters, transforms, and audits the dataset."""

    def __init__(self, min_dutiable_value: float = 0.0, exclude_country_iso: str = "UNK") -> None:
        self.min_dutiable_value = min_dutiable_value
        self.exclude_country_iso = exclude_country_iso
        self.audit_records: List[Dict[str, Any]] = []

    def check_missing_tq(self, df: pd.DataFrame) -> Tuple[int, int]:
        """Counts valid and missing (NaN) values in the 'tq' column without altering them."""
        missing_count = int(df["tq"].isna().sum())
        valid_count = int(df["tq"].notna().sum())
        return valid_count, missing_count

    def filter_records(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters dataset using two conditions via .loc."""
        cond1 = df["dutiablevaluephp"] > self.min_dutiable_value
        cond2 = (df["countryorigin_iso3"].notna()) & (df["countryorigin_iso3"] != self.exclude_country_iso)

        filtered_df = df.loc[cond1 & cond2].copy()

        if filtered_df.empty:
            raise ValueError(
                f"Filter error: No records met criteria "
                f"(dutiablevaluephp > {self.min_dutiable_value} AND countryorigin_iso3 != '{self.exclude_country_iso}')."
            )

        rule_desc = f"dutiablevaluephp > {self.min_dutiable_value} AND countryorigin_iso3 != '{self.exclude_country_iso}'"
        self.audit_records.append(
            compute_audit_step("Step_2_Filter", "FILTER", rule_desc, df, filtered_df)
        )

        return filtered_df

    def transform_and_sort(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates derived columns and sorts records descending."""
        df_transformed = df.copy()

        # Derived Column 1 (Numerical): Convert PHP value to Millions of PHP
        df_transformed["dutiablevalue_million_php"] = (
            df_transformed["dutiablevaluephp"] / 1_000_000.0
        )

        # Derived Column 2 (Category/Flag): Duty status flag
        if "duty" in df_transformed.columns:
            df_transformed["duty_paid_flag"] = np.where(
                df_transformed["duty"] > 0, "PAID", "EXEMPT_OR_ZERO"
            )
        else:
            df_transformed["duty_paid_flag"] = np.where(
                df_transformed["dutiablevaluephp"] >= 10000.0, "HIGH_VALUE", "LOW_VALUE"
            )

        # Sort dataset descending by primary value
        df_transformed = df_transformed.sort_values(
            by="dutiablevaluephp", ascending=False
        ).reset_index(drop=True)

        rule_desc = "Created 'dutiablevalue_million_php' & 'duty_paid_flag'; sorted by dutiablevaluephp desc"
        self.audit_records.append(
            compute_audit_step("Step_3_Transform", "TRANSFORM", rule_desc, df, df_transformed)
        )

        return df_transformed
