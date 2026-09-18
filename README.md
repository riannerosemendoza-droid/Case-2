# Case-2

# Philippine Customs 2015 Data Summary Program
## Group 4

| **Member** | **Assigned Task** | **Name** |
| ---------- | ----------------- | ------------------- |
| [Member 1 Name] | Data Loading and Inspection | Princess Kassy Mercado |
| [Member 2 Name] | Data Processing and Transformation | Rianne Rose Mendoza |
| [Member 3 Name] | Grouping and Summary Outputs | Keanna Lois Polvoriza |
| [Member 4 Name] | NumPy Analysis and Visualization | Arianne Denise Sumalinog |
| Olivia Patricia Jovita Baña | Validation and Documentation | Olivia Patricia Jovita Bana |

Final integration and testing were completed collaboratively by the group.

## Project Description

The Philippine Customs 2015 Data Summary Program is a Python-based application developed to process, summarize, analyze, visualize, and validate Philippine Customs data.

The program loads the Customs 2015 dataset, inspects the required fields, filters and transforms the records, creates grouped summaries and a pivot table, performs NumPy-based analysis, generates visualizations, and validates the results through reconciliation checks.

The project uses a modular structure in which the major stages of the data pipeline are separated into reusable Python modules. Git and GitHub were used for version control, branch-based development, code review, and integration.

## Project Features

The program provides the following major features:

1. **Data Loading and Inspection** – Loads the Customs 2015 CSV file and checks the required columns, row count, and initial numerical information.
2. **Data Processing and Transformation** – Filters records using defined conditions, sorts the selected records, and creates numerical and categorical derived columns.
3. **Data Grouping and Summarization** – Produces grouped summaries, a two-category summary, a pivot table, and a top-10 summary.
4. **NumPy Analysis** – Uses NumPy arrays, Boolean masking, vectorized calculations, aggregation, and a comparison between loop-based and vectorized calculations.
5. **Data Visualization** – Generates a bar chart and heatmap based on the summary outputs.
6. **Validation** – Reconciles row counts, numerical totals, summary tables, plot source values, and loop/vectorized calculations.
7. **Audit Logging** – Records major processing steps, operations, rules, and row counts in an audit log.

## Dataset Information

The project uses the Philippine Customs 2015 dataset from BetterGov.PH.

- **Dataset:** Philippine Customs 2015
- **Filename:** `2015.csv`
- **Source:** BetterGov.PH
- **Listed File Size:** 493.5 MB
- **Reference Row Count:** 2,236,612
- **Reference Column Count:** 30
- **Reference `dutiablevaluephp` Sum:** PHP 3,587,267,375,257
- **Verified SHA-256:** `b3b5a3a95340179a716a05611d51ad4906484d38363d1ac36494a404c04e4370`

The required fields for the analysis are:

- `countryorigin_iso3`
- `tq`
- `dutiablevaluephp`

The raw `2015.csv` file is not included in the repository or final submission archive. To run the program, the dataset must be placed in:

```text
data/2015.csv
```

## Installation and Requirements

The project requires Python and the following third-party libraries:

- NumPy
- pandas
- Matplotlib
- Seaborn

Install the required packages using:

```bash
pip install -r requirements.txt
```

Git is also used for version control and collaborative development.

## How to Run the Program

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd Case-2
```

Place the downloaded Customs dataset at:

```text
data/2015.csv
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the complete program:

```bash
python main.py
```

The program processes the dataset and generates the required summary, visualization, validation, and audit outputs.

## Repository Structure

The project is organized into separate modules based on their responsibilities:

```text
Case-2/
│
├── data/
│   └── 2015.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── processory.py
│   ├── summary_grouping.py
│   ├── analysis.py
│   └── validation.py
│
├── outputs/
│   ├── grouped.csv
│   ├── grouped_two.csv
│   ├── pivot.csv
│   ├── top10.csv
│   ├── bar.png
│   ├── heatmap.png
│   ├── validation.csv
│   └── audit_log.csv
│
├── main.py
├── config.py
├── requirements.txt
├── analysis.ipynb
├── analysis.html
├── contributions.md
├── submission_manifest.txt
├── .gitignore
└── README.md
```

## Module Descriptions

1. **data_loader.py** – Loads the raw CSV file, checks whether the required columns are present, and provides initial dataset summary information.

2. **processory.py** – Handles filtering, transformation, derived columns, sorting, and processing audit records.

3. **summary_grouping.py** – Creates `grouped.csv`, `grouped_two.csv`, `pivot.csv`, and `top10.csv` from the selected records.

4. **analysis.py** – Performs NumPy-based analysis, compares loop and vectorized calculations, measures their execution times, and generates the bar chart and heatmap.

5. **validation.py** – Performs reconciliation and reference checks and generates `validation.csv` and `audit_log.csv`.

6. **config.py** – Stores shared configuration values such as the dataset path, output path, and required columns.

7. **main.py** – Serves as the main entry point of the program and coordinates the complete data pipeline.

## Data Processing and Assumptions

The raw dataset is kept unchanged. Processing operations are performed on copies of the loaded data.

The program uses the following filtering conditions:

- `dutiablevaluephp > 0`
- `countryorigin_iso3` is not missing
- `countryorigin_iso3` is not equal to `UNK`

Records that do not satisfy the filtering conditions are treated as excluded records. Rows with missing values required by the filter are included in the excluded group.

Missing numerical values are reported as missing and are not replaced with zero. Grouping operations retain missing category groups where applicable using `dropna=False`.

Two derived columns are created:

- **`dutiablevalue_million_php`** – converts `dutiablevaluephp` from Philippine pesos to millions of Philippine pesos.
- **`value_flag`** – assigns `HIGH_VALUE` when `dutiablevaluephp` is greater than or equal to PHP 10,000 and `LOW_VALUE` otherwise.

Selected records are sorted by `dutiablevaluephp` in descending order.

The primary numerical measure, `dutiablevaluephp`, is expressed in Philippine pesos (PHP). The derived `dutiablevalue_million_php` field is expressed in millions of Philippine pesos.

## Output Files

The program generates the following outputs:

1. **grouped.csv** – Groups records by `countryorigin_iso3` and contains the row count, valid-measure count, measure sum, and measure mean.
2. **grouped_two.csv** – Groups records by `countryorigin_iso3` and `tq` and contains the row count and measure sum.
3. **pivot.csv** – Contains a pivot table of the sum of `dutiablevaluephp` across `countryorigin_iso3` and `tq`, including margins.
4. **top10.csv** – Contains the top 10 countries based on the measure sum from the first grouped summary.
5. **bar.png** – Displays the top 10 countries by total dutiable value.
6. **heatmap.png** – Displays dutiable values across countries of origin and TQ categories.
7. **validation.csv** – Records validation checks and their expected values, actual values, tolerances, and pass/fail results.
8. **audit_log.csv** – Records the processing step, operation, rule, rows before, and rows after each major stage.

## NumPy Analysis

The program converts the selected `dutiablevaluephp` values into a NumPy array and uses a Boolean mask to identify positive values.

A vectorized NumPy calculation and aggregation are performed on the data. A fixed-seed random sample is also used to compare a Python loop calculation with its NumPy equivalent.

The loop and NumPy calculations use the same sample. Their execution times are measured across five runs, and the median execution time for each approach is reported.

The results are validated to confirm that the loop-based and vectorized calculations agree.

## Visualizations

### Bar Chart

The bar chart uses the values from `top10.csv` and displays the top 10 countries according to total dutiable value.

- **X-axis:** Country of Origin
- **Y-axis:** Dutiable Value (PHP)

The bar chart provides a visual comparison of the countries with the highest total dutiable values in the selected Customs records.

### Heatmap

The heatmap uses the values from `pivot.csv` while excluding the total margins.

- **X-axis:** TQ
- **Y-axis:** Country of Origin
- **Values:** Dutiable Value (PHP)

The heatmap shows how total dutiable values are distributed across combinations of country of origin and TQ.

## Validation

The program generates `validation.csv` with the following columns:

- `check`
- `expected`
- `actual`
- `tolerance`
- `pass`

For Customs 2015, the program validates the dataset against the supplied reference values:

- **Rows:** 2,236,612
- **Columns:** 30
- **Raw `dutiablevaluephp` Sum:** PHP 3,587,267,375,257
- **Absolute Tolerance for Reference Sum:** PHP 1.00
- **Relative Tolerance:** 0
- **SHA-256:** `b3b5a3a95340179a716a05611d51ad4906484d38363d1ac36494a404c04e4370`

The validation process also checks that:

- raw rows equal selected rows plus excluded rows;
- rows with missing filter values are assigned to the excluded group;
- grouped row counts equal the selected row count;
- grouped sums equal an independently calculated sum of the selected measure;
- the pivot interior sum equals the independently calculated selected-measure sum without counting margins twice;
- values used for the bar chart match its summary table;
- values used for the heatmap match the pivot table without margins; and
- loop-based and vectorized calculations agree.

Counts are compared exactly. Numerical comparisons use declared floating-point tolerances. If a required validation check fails, the program displays the discrepancy and exits with a nonzero status.

## Audit Log

The program generates `audit_log.csv` with the following columns:

- `step`
- `operation`
- `rule`
- `rows_before`
- `rows_after`

The audit log documents the major stages of the pipeline and records the rules applied to the data. This provides a traceable record of how the raw dataset is loaded, filtered, transformed, summarized, analyzed, and validated.
