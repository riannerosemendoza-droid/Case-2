import csv
import sys
from pathlib import Path
from typing import Set

def valid_env(file_path: Path, req_cols: Set[str]) -> bool:
#check if the file exists before loading
    if not file_path.exists():
        print(f"Error: The file {file_path} does not exist.")
        return False

    print(f"File found: {file_path}")
    return True

class DataLoader:
#handles data using standard csv.

    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path
        self.rows: list[dict] = []
        self.fieldnames: list[str] = []

    def load_csv(self) -> None:
        print(f"Loading {self.file_path}... Please wait.")
        with open(self.file_path, mode="r", encoding="latin-1") as f:
            reader = csv.DictReader(f)
            self.fieldnames = reader.fieldnames or []
            self.rows = list(reader)
        print(f"Loaded {len(self.rows):,} records successfully!")
        return self.rows

    def check_required_columns(self, required_cols: Set[str]) -> bool:
        if not self.fieldnames:
            raise ValueError("Dataset not loaded. Call load_csv() first.")

        missing = required_cols - set(self.fieldnames)
        if missing:
            print(f"[ERROR] Missing required columns: {missing}")
            return False

        print("[OK] All required columns exist in the dataset.")
        return True

    def get_summary_stats(self) -> dict:
        if not self.rows:
            raise ValueError("Dataset not loaded. Call load_csv() first.")

        total_rows = len(self.rows)
        raw_sum = sum(
            float(row["dutiablevaluephp"])
            for row in self.rows    
            if row.get("dutiablevaluephp")
        )
        return {"total_rows": total_rows, "raw_sum": raw_sum}