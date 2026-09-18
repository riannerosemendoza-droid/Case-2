import config
from src.data_loader import DataLoader, valid_env

# 1. Verify file existence
if valid_env(config.file_path, config.req_cols):
    # 2. Instantiate and load data
    loader = DataLoader(config.file_path)
    loader.load_csv()

    # 3. Check for required columns
    loader.check_required_columns(config.req_cols)

    # 4. Display pipeline metrics
    stats = loader.get_summary_stats()
    print("\n--- PIPELINE RESULTS ---")
    print(f"Total Rows: {stats['total_rows']:,}")
    print(f"Raw Sum: PHP {stats['raw_sum']:,.2f}")