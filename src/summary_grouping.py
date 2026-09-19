
from pathlib import Path
from typing import Tuple

import pandas as pd


class SummaryGrouping:
    """Create summary tables from the processed DataFrame."""

    def __init__(
        self,
        output_folder: Path,
        group_column_1: str = "countryorigin_iso3",
        group_column_2: str = "tq",
        measure_column: str = "dutiablevaluephp"
    ) -> None:

        self.output_folder = output_folder
        self.group_column_1 = group_column_1
        self.group_column_2 = group_column_2
        self.measure_column = measure_column

        # Create the output folder if it does not exist.
        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def validate_columns(self, df: pd.DataFrame) -> None:
        """Check that all required grouping columns exist."""

        required_columns = {
            self.group_column_1,
            self.group_column_2,
            self.measure_column
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        print("[OK] Summary Grouping columns are present.")

    def create_grouped(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create grouped.csv.

        Groups by country and calculates:
        - row count
        - valid measure count
        - measure sum
        - measure mean
        """

        grouped = (
            df.groupby(
                self.group_column_1,
                dropna=False
            )
            .agg(
                row_count=(
                    self.measure_column,
                    "size"
                ),
                valid_measure_count=(
                    self.measure_column,
                    "count"
                ),
                measure_sum=(
                    self.measure_column,
                    "sum"
                ),
                measure_mean=(
                    self.measure_column,
                    "mean"
                )
            )
            .reset_index()
        )

        grouped = grouped.sort_values(
            by="measure_sum",
            ascending=False
        ).reset_index(drop=True)

        output_file = self.output_folder / "grouped.csv"

        grouped.to_csv(
            output_file,
            index=False
        )

        print(f"[OK] Created {output_file}")

        return grouped

    def create_grouped_two(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create grouped_two.csv.

        Groups by country + tq and calculates:
        - row count
        - measure sum
        """

        grouped_two = (
            df.groupby(
                [
                    self.group_column_1,
                    self.group_column_2
                ],
                dropna=False
            )
            .agg(
                row_count=(
                    self.measure_column,
                    "size"
                ),
                measure_sum=(
                    self.measure_column,
                    "sum"
                )
            )
            .reset_index()
        )

        grouped_two = grouped_two.sort_values(
            by="measure_sum",
            ascending=False
        ).reset_index(drop=True)

        output_file = (
            self.output_folder / "grouped_two.csv"
        )

        grouped_two.to_csv(
            output_file,
            index=False
        )

        print(f"[OK] Created {output_file}")

        return grouped_two

    def create_pivot(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create pivot.csv.

        Rows = countryorigin_iso3
        Columns = tq
        Values = sum of dutiablevaluephp
        Includes totals.
        """

        pivot = pd.pivot_table(
            df,
            index=self.group_column_1,
            columns=self.group_column_2,
            values=self.measure_column,
            aggfunc="sum",
            margins=True,
            margins_name="Total",
            dropna=False
        )

        pivot = pivot.reset_index()

        output_file = self.output_folder / "pivot.csv"

        pivot.to_csv(
            output_file,
            index=False
        )

        print(f"[OK] Created {output_file}")

        return pivot

    def create_top10(
        self,
        grouped: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create top10.csv.

        Uses grouped.csv data and keeps
        the 10 largest groups by measure_sum.
        """

        top10 = (
            grouped
            .sort_values(
                by="measure_sum",
                ascending=False
            )
            .head(10)
            .reset_index(drop=True)
        )

        output_file = self.output_folder / "top10.csv"

        top10.to_csv(
            output_file,
            index=False
        )

        print(f"[OK] Created {output_file}")

        return top10

    def create_all_summaries(
        self,
        df: pd.DataFrame
    ) -> Tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame
    ]:
        """Create all four required summary files."""

        self.validate_columns(df)

        grouped = self.create_grouped(df)

        grouped_two = self.create_grouped_two(df)

        pivot = self.create_pivot(df)

        top10 = self.create_top10(grouped)

        print(
            "\n[OK] All Summary Grouping outputs "
            "created successfully."
        )

        return (
            grouped,
            grouped_two,
            pivot,
            top10
        )    
if __name__ == "__main__":
    import os

    # Set base directory and output folder path
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "outputs"

    # Locate input dataset (looks in data/2015.csv first)
    input_file = base_dir / "data" / "2015.csv"

    if not input_file.exists():
        # Fallback search for other possible file names/locations
        possible_inputs = [
            base_dir / "outputs" / "filtered.csv",
            base_dir / "filtered_data.csv",
            base_dir / "2015.csv"
        ]
        input_file = next((f for f in possible_inputs if f.exists()), None)

    if input_file and input_file.exists():
        print(f"Loading data from: {input_file}")
        df_raw = pd.read_csv(input_file, encoding="latin-1", low_memory=False)

        # Instantiate class and create outputs
        summarizer = SummaryGrouping(output_folder=output_dir)
        summarizer.create_all_summaries(df_raw)
    else:
        print("[ERROR] No valid CSV dataset found in data/ or root directory.")