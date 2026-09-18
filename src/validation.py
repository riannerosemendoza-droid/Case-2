"""
Validation Module

Checks whether the Philippine Customs 2015 data pipeline
produces the expected data, calculations, and output files.
"""

from pathlib import Path
import numpy as np
import pandas as pd

def validate_required_columns(df: pd.DataFrame, required_columns: set) -> bool:
    """Check whether all required columns are present."""
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(f"[FAIL] Missing required columns: {sorted(missing_columns)}")
        return False
    print("[PASS] All required columns are present.")
    return True

def validate_raw_data(df: pd.DataFrame, expected_rows: int, expected_sum: float) -> bool:
    """Check the raw row count and dutiable value sum."""
    actual_rows = len(df)
    values = pd.to_numeric(df["dutiablevaluephp"], errors="coerce")
    actual_sum = values.sum()
    rows_match = actual_rows == expected_rows
    sum_match = np.isclose(actual_sum, expected_sum)

    if rows_match:
        print(f"[PASS] Row count: {actual_rows:,}")
    else:
        print(f"[FAIL] Row count: {actual_rows:,} (expected {expected_rows:,})")
      
    if sum_match:
        print(f"[PASS] Raw sum: PHP {actual_sum:,.2f}")
    else:
        print(f"[FAIL] Raw sum: PHP {actual_sum:,.2f} (expected PHP {expected_sum:,.2f})")

    return bool(rows_match and sum_match)

def validate_processed_data(df: pd.DataFrame) -> bool:
    """Check whether processed data contains valid derived values."""
    required_columns = {"dutiablevaluephp", "dutiablevalue_million_php", "value_flag"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(f"[FAIL] Missing processed columns: {sorted(missing_columns)}")
        return False

    expected_million = df["dutiablevaluephp"] / 1_000_000
    million_match = np.allclose(df["dutiablevalue_million_php"], expected_million)
    expected_flag = np.where(df["dutiablevaluephp"] >= 10_000, "HIGH_VALUE", "LOW_VALUE")
    flag_match = np.array_equal(df["value_flag"].to_numpy(), expected_flag)
    sorted_correctly = df["dutiablevaluephp"].is_monotonic_decreasing

    if million_match:
        print("[PASS] Million-PHP conversion is correct.")
    else:
        print("[FAIL] Million-PHP conversion is incorrect.")

    if flag_match:
        print("[PASS] Value flags are correct.")
    else:
        print("[FAIL] Value flags are incorrect.")

    if sorted_correctly:
        print("[PASS] Records are sorted by dutiable value descending.")
    else:
        print("[FAIL] Records are not sorted correctly.")

    return bool(million_match and flag_match and sorted_correctly)

def validate_analysis_results(results: dict) -> bool:
    """Check whether loop and NumPy calculations match."""
    results_match = bool(results.get("results_match", False))

    if results_match:
        print("[PASS] Loop and NumPy results match.")
        return True
    print("[FAIL] Loop and NumPy results do not match.")
    return False

def validate_output_files(output_folder: Path) -> bool:
    """Check whether all required output files exist."""
    required_files = ["grouped.csv", "grouped_two.csv", "pivot.csv", "top10.csv", "bar.png", "heatmap.png"]
    all_exist = True

    for filename in required_files:
        file_path = output_folder / filename

        if file_path.exists():
            print(f"[PASS] Found {filename}")
        else:
            print(f"[FAIL] Missing {filename}")
            all_exist = False

    return all_exist
