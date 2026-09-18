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


def compute_audit_step(
    step: str,
    operation: str,
    rule: str,
    df_before: pd.DataFrame,
    df_after: pd.DataFrame
) -> Dict[str, Any]:
    """Create an audit record showing the rows before and after a step."""

    # Store information about what happened during the processing step
    return {
        "step": step,
        "operation": operation,
        "rule": rule,
        "rows_before": len(df_before),
        "rows_after": len(df_after)
    }


class DataProcessor:
    """Handles filtering, transformation, sorting, and auditing."""

    def __init__(
        self,
        min_dutiable_value: float = 0.0,
        exclude_country_iso: str = "UNK"
    ) -> None:
        """Set the filtering rules and create an empty audit log."""

        # Minimum dutiable value allowed in the filtered records
        self.min_dutiable_value = min_dutiable_value

        # Country code that will be excluded
        self.exclude_country_iso = exclude_country_iso

        # Stores the processing steps for the audit log
        self.audit_records: List[Dict[str, Any]] = []

    def check_missing_tq(
        self,
        df: pd.DataFrame
    ) -> Tuple[int, int]:
        """Count valid and missing values in the tq column."""

        # Count missing tq values
        missing_count = int(df["tq"].isna().sum())

        # Count tq values that are not missing
        valid_count = int(df["tq"].notna().sum())

        return valid_count, missing_count

    def filter_records(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """Filter records using two conditions with .loc."""

        # Make a copy so the original DataFrame is not changed
        df = df.copy()

        # Convert dutiablevaluephp to a numerical data type.
        # Invalid or blank numerical values become NaN.
        df["dutiablevaluephp"] = pd.to_numeric(
            df["dutiablevaluephp"],
            errors="coerce"
        )

        # FILTERING CONDITIONS

        # Condition 1:
        # Keep records where dutiablevaluephp is greater than PHP 0.
        condition_1 = (
            df["dutiablevaluephp"] > self.min_dutiable_value
        )

        # Condition 2:
        # Keep records where countryorigin_iso3 is not missing
        # and is not equal to "UNK".
        condition_2 = (
            df["countryorigin_iso3"].notna()
            & (df["countryorigin_iso3"] != self.exclude_country_iso)
        )

        # Use .loc and require BOTH conditions to be true.
        filtered_df = df.loc[
            condition_1 & condition_2
        ].copy()

        # If no records remain, show a clear error message.
        if filtered_df.empty:
            raise ValueError(
                "No records matched the filtering conditions."
            )

        # Describe the filtering rule for the audit log.
        rule_desc = (
            f"dutiablevaluephp > {self.min_dutiable_value} AND "
            f"countryorigin_iso3 is not missing AND "
            f"countryorigin_iso3 != '{self.exclude_country_iso}'"
        )

        # Record the filtering operation in the audit log.
        self.audit_records.append(
            compute_audit_step(
                "Step_2_Filter",
                "FILTER",
                rule_desc,
                df,
                filtered_df
            )
        )

        return filtered_df

    def transform_and_sort(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """Create two derived columns and sort the records."""

        # Make a copy so the filtered DataFrame is not directly changed
        df_transformed = df.copy()

 
        # DERIVED COLUMN 1: NUMERICAL
 

        # Convert dutiablevaluephp from PHP to millions of PHP.
        # Example: PHP 2,000,000 becomes 2.0.
        df_transformed["dutiablevalue_million_php"] = (
            df_transformed["dutiablevaluephp"] / 1_000_000
        )

        # DERIVED COLUMN 2: CATEGORY / FLAG
   

        # Classify records based on their dutiable value.
        # PHP 10,000 or higher = HIGH_VALUE.
        # Below PHP 10,000 = LOW_VALUE.
        df_transformed["value_flag"] = np.where(
            df_transformed["dutiablevaluephp"] >= 10_000,
            "HIGH_VALUE",
            "LOW_VALUE"
        )

 
        # SORTING
    

        # Sort records from the highest dutiable value
        # to the lowest dutiable value.
        df_transformed = df_transformed.sort_values(
            by="dutiablevaluephp",
            ascending=False
        ).reset_index(drop=True)

        # Describe the transformations for the audit log.
        rule_desc = (
            "Created dutiablevalue_million_php and value_flag; "
            "sorted by dutiablevaluephp descending"
        )

        # Record the transformation operation in the audit log.
        self.audit_records.append(
            compute_audit_step(
                "Step_3_Transform",
                "TRANSFORM",
                rule_desc,
                df,
                df_transformed
            )
        )

        return df_transformed
