# Case-2

## Philippine Customs 2015 Data Summary Program
#### Group 4

| **Member** | **Assigned Task** | **Name** |
| ---------- | ----------------- | ------------------- |
|  Member 1  | Data Loading and Inspection | Princess Kassy Mercado |
|  Member 2  | Data Processing and Transformation | Rianne Rose Mendoza |
|  Member 3  | Grouping and Summary Outputs | Keanna Lois Polvoriza |
|  Member 4  | NumPy Analysis and Visualization | Arianne Denise Sumalinog |
| Member 5   | Validation and Documentation | Olivia Patricia Jovita Bana |

Final integration and testing were completed collaboratively by the group.


### Project Overview

This project is a Python-based data summary program developed for DSA4153 – Programming for Data Science, Summative Lab Exercise Case Study No. 2. The program processes the Philippine Customs 2015 dataset from BetterGov.PH and demonstrates data loading, filtering, transformation, aggregation, visualization, NumPy-based analysis, validation, and audit logging. The program uses a modular structure in which separate Python modules handle data loading, data processing, summary generation, analysis and visualization, and validation. The complete program is designed to run through main.py and generate the required summary tables, plots, validation results, and audit records.


### Dataset Information
**Dataset**: Philippine Customs 2015

**Filename**: 2015.csv

**Source**: BetterGov.PH

**Source URL**: https://data.bettergov.ph/datasets/21

**Download Date**: 2026-09-18

**File Size**: 493.5 MB

**File Format**: CSV

The raw dataset contains 2,236,612 rows and 30 columns. The reference total for dutiablevaluephp is PHP 3,587,267,375,257.00.

The raw 2015.csv dataset is not included in the repository or submission ZIP because of its large file size. Before running the program, download the dataset from the source above and place it inside the data folder using the filename 2015.csv.


### Required Dataset Fields

The program uses the following fields from the Philippine Customs dataset:

**countryorigin_iso3** – Country of origin represented using an ISO3 country code.

**tq** – Second categorical field used for the two-category grouping and pivot table.

**dutiablevaluephp** – Numerical measure representing dutiable value in Philippine pesos (PHP).


### Project Structure

The project is organized into separate modules based on their responsibilities.

**main.py** - Serves as the main entry point of the program and executes the complete data-processing pipeline.

**config.py** - Contains configuration values such as the dataset path, output directory, and required dataset columns.

**src/data_loader.py** - Handles loading the Customs CSV file, checking required columns, and obtaining initial raw dataset statistics.

**src/processory.py** - Handles data filtering, transformation, derived columns, sorting, and processing audit records.

**src/summary_grouping.py** - Creates the grouped summaries, two-category summary, pivot table, and Top 10 summary.

**src/analysis.py** - Performs the NumPy analysis, Boolean masking, vectorized calculation, loop-versus-NumPy comparison, and creation of the required plots.

**src/validation.py** - Performs validation and reconciliation checks and generates validation.csv and audit_log.csv.

**src/__init__.py** - Initializes the src package.

**outputs folder** - Contains the generated CSV summaries, plots, validation results, and audit log.

**analysis.ipynb** - Contains the notebook version of the analysis.

**analysis.html** - Contains the exported HTML version of the analysis notebook.

**contributions.md** - Documents the individual contributions and review records of the group members.

**submission_manifest.txt** - Records the repository URL, submitted release tag, and full commit hash.


### Setup
Python is required to run the program.

The project uses the following Python libraries:

**pandas**

**NumPy**

**Matplotlib**

**Seaborn**

The required packages can be installed using requirements.txt.

Place the downloaded dataset in the following location before running the program:
data/2015.csv


### Running the Program
From the root directory of the repository, run:
main.py

The program loads the dataset, checks the required fields, inspects the raw data, processes the selected records, creates the required summaries and plots, performs the NumPy analysis, and runs the validation checks.

If a required validation check fails, the program reports the discrepancy and exits with a nonzero status.


### Data Inspection
Before processing, the program inspects the dataset row count, number of columns, column data types, and missing values.

The dutiablevaluephp field is converted to a numerical data type for processing and validation. Missing numerical values are counted and reported separately rather than being replaced with zero.


### Filtering Rules
The program uses two filtering conditions to select records for further processing.

A record is selected when:
dutiablevaluephp > 0
AND
countryorigin_iso3 is not missing and is not equal to "UNK"

The filtering operation is performed using pandas .loc.

Records that do not satisfy the filtering conditions are treated as excluded records. Records with missing values in fields required by the filter are included in the excluded count according to the filtering rule.

The same selected records are used as the source for all six required primary outputs.


### Transformation Rules
After filtering, the program creates two derived columns.

**dutiablevalue_million_php** - A numerical derived column calculated by dividing dutiablevaluephp by 1,000,000.

**value_flag** - A categorical derived column. Records with dutiablevaluephp greater than or equal to PHP 10,000 are classified as HIGH_VALUE, while values below PHP 10,000 are classified as LOW_VALUE.

The processed records are then sorted by dutiablevaluephp in descending order.


### Missing Value Handling
Missing categorical values are retained as explicit groups where applicable during grouping operations. Missing numerical values are reported separately and are not replaced with zero. Records with missing values required by the filtering rule are excluded according to the stated filter conditions.The raw dataset is not modified by the program.


### Units
The primary numerical measure, dutiablevaluephp, is expressed in Philippine pesos (PHP).

The derived dutiablevalue_million_php field expresses the same measure in millions of Philippine pesos.

Summary totals, means, Top 10 values, and visualization values based on dutiablevaluephp therefore use PHP as their monetary unit.


### Generated Summary Outputs
The program generates the following four summary CSV files.

**grouped.csv** - Groups the selected records by countryorigin_iso3 and reports the row count, valid-measure count, measure sum, and measure mean.

**grouped_two.csv** - Groups the selected records by countryorigin_iso3 and tq and reports the row count and measure sum using named aggregations.

**pivot.csv** - Creates a pivot table showing the sum of dutiablevaluephp across countryorigin_iso3 and tq, including margins.

**top10.csv** - Sorts the first grouped summary by measure sum in descending order and keeps the ten largest groups.


### Visualizations

**bar.png** - A Matplotlib bar chart generated from top10.csv. It shows the Top 10 countries of origin based on total dutiable value in Philippine pesos.

**heatmap.png** - A Seaborn heatmap generated from pivot.csv after excluding the pivot margins. It visualizes dutiable value across countryorigin_iso3 and tq combinations.


### NumPy Analysis and Performance Comparison
The analysis module converts dutiablevaluephp values into a NumPy array and uses a Boolean mask to select positive values. A vectorized NumPy calculation is then used to aggregate the selected values. The program also compares a loop-based calculation with its NumPy vectorized equivalent using the same fixed-seed sample. A random number generator with seed 42 is used to create a sample of up to 100,000 values. Both approaches are timed over five runs, and their median execution times are reported. The resulting calculations are also checked for agreement.


### Validation
The program generates validation.csv with the following columns:

check, expected, actual, tolerance, pass

The validation process checks the raw dataset against the provided Customs 2015 reference values:

**Expected rows**: 2,236,612

**Expected columns**: 30

**Expected dutiablevaluephp total**: PHP 3,587,267,375,257.00

**Absolute numerical tolerance**: PHP 1.00

**Relative tolerance**: 0

The validation process also checks that raw rows reconcile with selected and excluded rows, the filtering rule produces the expected selected and excluded counts, missing filter-value rows are excluded, grouped row counts equal the selected row count, grouped and pivot totals reconcile with an independently calculated selected measure total, the plot source values agree with their summary tables, and the loop and vectorized calculations agree.

Pivot margins are excluded when the pivot interior total is validated to prevent totals from being counted more than once.

If any validation check fails, the discrepancy is displayed and the program exits with a nonzero status.


### Audit Log
The program generates audit_log.csv with the following columns:

step, operation, rule, rows_before, rows_after

The audit log records the major stages of the pipeline, including loading, filtering, transformation, summary generation, analysis and plotting, and validation. It records the processing rule used at each stage and the number of records before and after the operation.


### Generated Files
The complete pipeline produces the following required outputs:

outputs/grouped.csv

outputs/grouped_two.csv

outputs/pivot.csv

outputs/top10.csv

outputs/bar.png

outputs/heatmap.png

outputs/validation.csv

outputs/audit_log.csv


### Git and Collaboration
The project was developed collaboratively using Git and GitHub. Group members contributed to separate components of the program and participated in debugging and testing the integrated pipeline. Individual contributions are documented in contributions.md.

The final submitted version of the project is identified using the Git tag:
week6-v1.0

Repository and final commit information are recorded in submission_manifest.txt.
