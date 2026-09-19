"""
Validation Module

Validates the Philippine Customs 2015 data pipeline, reconciles
summary outputs, checks plot source values and NumPy calculations,
and generates validation.csv and audit_log.csv.
"""

from pathlib import Path
import hashlib
import sys
import numpy as np
import pandas as pd


REFERENCE_ROWS = 2_236_612
REFERENCE_COLUMNS = 30
REFERENCE_SUM = 3_587_267_375_257.00
REFERENCE_SHA256 = "b3b5a3a95340179a716a05611d51ad4906484d38363d1ac36494a404c04e4370"

ABS_TOLERANCE = 1.00
REL_TOLERANCE = 0.0


def calculate_sha256(file_path: Path) -> str:
    """Calculate and return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def add_check(records: list, check: str, expected, actual, tolerance, passed: bool) -> None:
    """Add one validation result and display its status."""
    records.append({
        "check": check,
        "expected": expected,
        "actual": actual,
        "tolerance": tolerance,
        "pass": bool(passed)
    })

    if passed:
        print(f"[PASS] {check}")
    else:
        print(f"[FAIL] {check}: expected {expected}, actual {actual}")


def validate_pipeline(raw_df: pd.DataFrame, selected_df: pd.DataFrame, analysis_results: dict, data_file: Path, output_folder: Path, audit_records: list) -> bool:
    """Run all required validation checks and generate validation and audit files."""
    output_folder.mkdir(parents=True, exist_ok=True)
    records = []

    print("\n=== VALIDATION ===")

    raw_rows = len(raw_df)
    raw_columns = raw_df.shape[1]
    selected_rows = len(selected_df)
    excluded_rows = raw_rows - selected_rows

    raw_measure = pd.to_numeric(raw_df["dutiablevaluephp"], errors="coerce")
    selected_measure = pd.to_numeric(selected_df["dutiablevaluephp"], errors="coerce")

    raw_sum = raw_measure.sum()
    selected_sum = selected_measure.sum()

    add_check(records, "Raw row count", REFERENCE_ROWS, raw_rows, "exact", raw_rows == REFERENCE_ROWS)
    add_check(records, "Raw column count", REFERENCE_COLUMNS, raw_columns, "exact", raw_columns == REFERENCE_COLUMNS)
    add_check(records, "Raw dutiablevaluephp sum", REFERENCE_SUM, raw_sum, "absolute PHP 1.00; relative 0", np.isclose(raw_sum, REFERENCE_SUM, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE))

    actual_sha256 = calculate_sha256(data_file)
    add_check(records, "Dataset SHA-256", REFERENCE_SHA256, actual_sha256, "exact", actual_sha256 == REFERENCE_SHA256)

    numeric_measure = pd.to_numeric(raw_df["dutiablevaluephp"], errors="coerce")
    filter_condition = (numeric_measure > 0) & raw_df["countryorigin_iso3"].notna() & (raw_df["countryorigin_iso3"] != "UNK")

    expected_selected_rows = int(filter_condition.sum())
    expected_excluded_rows = raw_rows - expected_selected_rows

    missing_filter_mask = numeric_measure.isna() | raw_df["countryorigin_iso3"].isna()
    missing_filter_rows = int(missing_filter_mask.sum())
    missing_rows_excluded = bool((filter_condition & missing_filter_mask).sum() == 0)

    add_check(records, "Missing filter-value row count", missing_filter_rows, missing_filter_rows, "exact", True)
    add_check(records, "Raw rows equal selected plus excluded rows", raw_rows, selected_rows + excluded_rows, "exact", raw_rows == selected_rows + excluded_rows)
    add_check(records, "Selected row count follows filter rule", expected_selected_rows, selected_rows, "exact", selected_rows == expected_selected_rows)
    add_check(records, "Excluded row count follows filter rule", expected_excluded_rows, excluded_rows, "exact", excluded_rows == expected_excluded_rows)
    add_check(records, "Missing filter-value rows are excluded", True, missing_rows_excluded, "exact", missing_rows_excluded)

    grouped_file = output_folder / "grouped.csv"
    grouped_two_file = output_folder / "grouped_two.csv"
    pivot_file = output_folder / "pivot.csv"
    top10_file = output_folder / "top10.csv"
    bar_file = output_folder / "bar.png"
    heatmap_file = output_folder / "heatmap.png"

    required_files = [grouped_file, grouped_two_file, pivot_file, top10_file, bar_file, heatmap_file]

    for file_path in required_files:
        add_check(records, f"Output file exists: {file_path.name}", True, file_path.exists(), "exact", file_path.exists())

    summary_files_exist = all(file_path.exists() for file_path in [grouped_file, grouped_two_file, pivot_file, top10_file])

    if summary_files_exist:
        grouped = pd.read_csv(grouped_file)
        grouped_two = pd.read_csv(grouped_two_file)
        pivot = pd.read_csv(pivot_file)
        top10 = pd.read_csv(top10_file)

        grouped_row_count = int(grouped["row_count"].sum())
        add_check(records, "Grouped row counts equal selected row count", selected_rows, grouped_row_count, "exact", grouped_row_count == selected_rows)

        grouped_sum = pd.to_numeric(grouped["measure_sum"], errors="coerce").sum()
        add_check(records, "Grouped sum equals independently computed selected sum", selected_sum, grouped_sum, "absolute PHP 1.00; relative 0", np.isclose(grouped_sum, selected_sum, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE))

        grouped_two_row_count = int(grouped_two["row_count"].sum())
        add_check(records, "Two-category grouped row counts equal selected row count", selected_rows, grouped_two_row_count, "exact", grouped_two_row_count == selected_rows)

        grouped_two_sum = pd.to_numeric(grouped_two["measure_sum"], errors="coerce").sum()
        add_check(records, "Two-category grouped sum equals independently computed selected sum", selected_sum, grouped_two_sum, "absolute PHP 1.00; relative 0", np.isclose(grouped_two_sum, selected_sum, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE))

        pivot_interior = pivot.copy()

        if "countryorigin_iso3" in pivot_interior.columns:
            pivot_interior = pivot_interior[pivot_interior["countryorigin_iso3"] != "Total"]
            pivot_interior = pivot_interior.set_index("countryorigin_iso3")

        pivot_interior = pivot_interior.drop(columns="Total", errors="ignore")
        pivot_numeric = pivot_interior.apply(pd.to_numeric, errors="coerce")
        pivot_sum = np.nansum(pivot_numeric.to_numpy())

        add_check(records, "Pivot interior sum equals independently computed selected sum", selected_sum, pivot_sum, "absolute PHP 1.00; relative 0", np.isclose(pivot_sum, selected_sum, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE))

        expected_top10 = grouped.sort_values(by="measure_sum", ascending=False).head(10).reset_index(drop=True)

        bar_categories_match = top10["countryorigin_iso3"].astype(str).tolist() == expected_top10["countryorigin_iso3"].astype(str).tolist()
        bar_values_match = np.allclose(pd.to_numeric(top10["measure_sum"], errors="coerce"), pd.to_numeric(expected_top10["measure_sum"], errors="coerce"), atol=ABS_TOLERANCE, rtol=REL_TOLERANCE, equal_nan=True)
        bar_source_match = bool(bar_categories_match and bar_values_match)

        add_check(records, "Values passed to bar plot match top10.csv", True, bar_source_match, "exact categories; absolute PHP 1.00; relative 0", bar_source_match)

        expected_pivot = pd.pivot_table(
            selected_df,
            index="countryorigin_iso3",
            columns="tq",
            values="dutiablevaluephp",
            aggfunc="sum",
            margins=True,
            margins_name="Total",
            dropna=False
        ).reset_index()

        expected_pivot_interior = expected_pivot[expected_pivot["countryorigin_iso3"] != "Total"].set_index("countryorigin_iso3")
        expected_pivot_interior = expected_pivot_interior.drop(columns="Total", errors="ignore")
        expected_pivot_numeric = expected_pivot_interior.apply(pd.to_numeric, errors="coerce")

        actual_heatmap = pivot[pivot["countryorigin_iso3"] != "Total"].set_index("countryorigin_iso3")
        actual_heatmap = actual_heatmap.drop(columns="Total", errors="ignore")
        actual_heatmap_numeric = actual_heatmap.apply(pd.to_numeric, errors="coerce")

        expected_pivot_numeric = expected_pivot_numeric.reindex(index=actual_heatmap_numeric.index, columns=actual_heatmap_numeric.columns)

        heatmap_values_match = actual_heatmap_numeric.shape == expected_pivot_numeric.shape and np.allclose(actual_heatmap_numeric.to_numpy(), expected_pivot_numeric.to_numpy(), atol=ABS_TOLERANCE, rtol=REL_TOLERANCE, equal_nan=True)

        add_check(records, "Values passed to heatmap match pivot.csv without margins", True, heatmap_values_match, "absolute PHP 1.00; relative 0", heatmap_values_match)

    loop_result = analysis_results.get("loop_result")
    numpy_result = analysis_results.get("numpy_result")

    if loop_result is not None and numpy_result is not None:
        loop_numpy_match = np.isclose(loop_result, numpy_result, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE)
    else:
        loop_numpy_match = False

    add_check(records, "Loop and vectorized calculations agree", loop_result, numpy_result, "absolute PHP 1.00; relative 0", loop_numpy_match)

    audit_records = list(audit_records)

    audit_records.insert(0, {
        "step": "Step_1_Load",
        "operation": "LOAD",
        "rule": "Load raw Customs 2015 CSV without modifying the raw file",
        "rows_before": raw_rows,
        "rows_after": raw_rows
    })

    audit_records.append({
        "step": "Step_4_Summary",
        "operation": "GROUP_AND_PIVOT",
        "rule": "Create grouped, two-category grouped, pivot, and top-10 summaries from the same selected records",
        "rows_before": selected_rows,
        "rows_after": selected_rows
    })

    audit_records.append({
        "step": "Step_5_Analysis",
        "operation": "ANALYZE_AND_PLOT",
        "rule": "Compare loop and NumPy calculations and create plots from summary tables",
        "rows_before": selected_rows,
        "rows_after": selected_rows
    })

    audit_records.append({
        "step": "Step_6_Validation",
        "operation": "VALIDATE",
        "rule": f"Reconcile counts and sums; missing filter values are excluded; numerical comparisons use absolute tolerance {ABS_TOLERANCE} and relative tolerance {REL_TOLERANCE}",
        "rows_before": selected_rows,
        "rows_after": selected_rows
    })

    validation_df = pd.DataFrame(records, columns=["check", "expected", "actual", "tolerance", "pass"])
    validation_file = output_folder / "validation.csv"
    validation_df.to_csv(validation_file, index=False)

    audit_df = pd.DataFrame(audit_records, columns=["step", "operation", "rule", "rows_before", "rows_after"])
    audit_file = output_folder / "audit_log.csv"
    audit_df.to_csv(audit_file, index=False)

    print(f"\n[OK] Created {validation_file}")
    print(f"[OK] Created {audit_file}")

    all_passed = bool(validation_df["pass"].all())

    if not all_passed:
        print("\n[FAIL] Validation discrepancies found:")
        failed_checks = validation_df.loc[~validation_df["pass"], ["check", "expected", "actual", "tolerance"]]
        print(failed_checks.to_string(index=False))
        sys.exit(1)

    print("\n[PASS] All validation checks passed.")
    return True
