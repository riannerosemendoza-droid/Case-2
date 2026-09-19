import pandas as pd

import config

from src.data_loader import DataLoader
from src.processory import DataProcessor
from src.summary_grouping import SummaryGrouping
from src.analysis import run_analysis
from src.validation import validate_pipeline


def main() -> None:
    """Run the Customs 2015 data pipeline."""

    print("CUSTOMS 2015 DATA PIPELINE")

    # Step 1: Load the data
    print("\n--- Step 1: Loading Data ---")

    loader = DataLoader(config.file_path)
    loader.load_csv()

    if not loader.check_required_columns(config.req_cols):
        raise ValueError("Required columns are missing from the dataset.")

    raw_df = pd.DataFrame(loader.rows)

    print(f"Raw dataset shape: {raw_df.shape}")

    # Step 2: Process the data
    print("\n--- Step 2: Processing Data ---")

    processor = DataProcessor(
        min_dutiable_value=0.0,
        exclude_country_iso="UNK"
    )

    valid_tq, missing_tq = processor.check_missing_tq(raw_df)

    print(f"Valid TQ values: {valid_tq:,}")
    print(f"Missing TQ values: {missing_tq:,}")

    selected_df = processor.filter_records(raw_df)
    selected_df = processor.transform_and_sort(selected_df)

    print(f"Selected records: {len(selected_df):,}")

    # Step 3: Create summary tables
    print("\n--- Step 3: Creating Summary Tables ---")

    summary = SummaryGrouping(output_folder=config.output_path)

    grouped, grouped_two, pivot, top10 = summary.create_all_summaries(
        selected_df
    )

    print("[OK] Created grouped.csv")
    print("[OK] Created grouped_two.csv")
    print("[OK] Created pivot.csv")
    print("[OK] Created top10.csv")

    # Step 4: NumPy analysis and plots
    print("\n--- Step 4: NumPy Analysis and Plots ---")

    analysis_results = run_analysis(selected_df)

    print("\nNumPy Analysis Results:")

    for key, value in analysis_results.items():
        print(f"{key}: {value}")

    # Step 5: Validation
    print("\n--- Step 5: Validation ---")

    validate_pipeline(
        raw_df=raw_df,
        selected_df=selected_df,
        analysis_results=analysis_results,
        data_file=config.file_path,
        output_folder=config.output_path,
        audit_records=processor.audit_records
    )

    print("\nPIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
