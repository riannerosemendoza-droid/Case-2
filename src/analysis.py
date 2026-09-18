import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import config


def loop_sum(values: np.ndarray) -> float:
    """Calculate the sum of positive values using a loop."""
    total = 0.0

    for value in values:
        if value > 0:
            total += value

    return total


def numpy_sum(values: np.ndarray) -> float:
    """Calculate the sum of positive values using NumPy."""
    return np.sum(values[values > 0])


def compare_loop_and_numpy(values: np.ndarray) -> dict:
    """Compare loop and NumPy calculations and their running times."""

    loop_times = []
    numpy_times = []

    for _ in range(5):
        start = time.perf_counter()
        loop_result = loop_sum(values)
        loop_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        numpy_result = numpy_sum(values)
        numpy_times.append(time.perf_counter() - start)

    loop_median = np.median(loop_times)
    numpy_median = np.median(numpy_times)

    return {
        "loop_result": loop_result,
        "numpy_result": numpy_result,
        "results_match": np.isclose(loop_result, numpy_result),
        "loop_median_time": loop_median,
        "numpy_median_time": numpy_median
    }


def run_numpy_analysis(df: pd.DataFrame) -> dict:
    """Run NumPy array, mask, vectorized calculation, and timing."""

    values = df["dutiablevaluephp"].to_numpy(dtype=float)

    positive_mask = values > 0
    positive_values = values[positive_mask]

    vectorized_total = np.sum(positive_values)

    rng = np.random.default_rng(42)
    sample_size = min(100000, len(values))
    sample = rng.choice(values, size=sample_size, replace=False)

    results = compare_loop_and_numpy(sample)

    results["total_values"] = len(values)
    results["positive_values"] = len(positive_values)
    results["vectorized_total"] = vectorized_total
    results["sample_size"] = sample_size

    return results


def create_bar_chart(
    top10_file: str,
    output_file: str
) -> None:
    """Create a bar chart of the top 10 countries."""

    top10 = pd.read_csv(top10_file)

    plt.figure(figsize=(10, 6))

    plt.bar(
        top10["countryorigin_iso3"],
        top10["measure_sum"]
    )

    plt.title("Top 10 Countries by Dutiable Value")
    plt.xlabel("Country of Origin")
    plt.ylabel("Dutiable Value (PHP)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()


def create_heatmap(
    pivot_file: str,
    output_file: str
) -> None:
    """Create a heatmap from the pivot table without totals."""

    pivot = pd.read_csv(pivot_file)

    pivot = pivot.set_index("countryorigin_iso3")

    pivot = pivot.drop(
        index="Total",
        errors="ignore"
    )

    pivot = pivot.drop(
        columns="Total",
        errors="ignore"
    )

    plt.figure(figsize=(12, 8))

    sns.heatmap(
        pivot,
        annot=False,
        cmap="viridis"
    )

    plt.title("Dutiable Value by Country and TQ")
    plt.xlabel("TQ")
    plt.ylabel("Country of Origin")

    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()


def run_analysis(df: pd.DataFrame) -> dict:
    """Run the NumPy analysis and create the required plots."""

    numpy_results = run_numpy_analysis(df)

    top10_file = config.output_path / "top10.csv"
    pivot_file = config.output_path / "pivot.csv"

    bar_file = config.output_path / "bar.png"
    heatmap_file = config.output_path / "heatmap.png"

    create_bar_chart(
        str(top10_file),
        str(bar_file)
    )

    create_heatmap(
        str(pivot_file),
        str(heatmap_file)
    )

    return numpy_results