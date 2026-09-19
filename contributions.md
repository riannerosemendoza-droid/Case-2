### Member 1 (Data Loading and Setup)
**Name: Princess Kassy Mercado**

**Github Username: pkkmercado**

Member 1 was responsible for the data loading component of the project. They developed data_loader.py, which handles loading the Philippine Customs 2015 CSV dataset, 
checking whether the required columns are present, and obtaining the initial dataset statistics such as the total number of rows and the raw sum of dutiablevaluephp. 
They also participated in debugging and testing the program to help ensure that the data loading component worked correctly with the other modules.


### Member 2 (Data Processing and Transformation)
**Name: Rianne Rose Mendoza**

**Github Username: riannerosemendoza-droid**

Member 2 was responsible for data processing and transformation. They developed processory.py, which applies the filtering conditions using .loc, converts dutiablevaluephp 
into a numerical data type, creates the derived numerical and categorical columns, sorts the processed records, and records processing information for the audit trail. They 
also participated in debugging and testing the program, particularly in checking the processing and transformation of the dataset.


### Member 3 (Summary and Grouping)
**Name: Keanna Lois Polvoriza**

**Github Username: keannaloispolvoriza**

Member 3 was responsible for summary grouping and aggregation. They developed summary_grouping.py, which creates the one-category grouped summary, two-category grouped summary, 
pivot table, and Top 10 summary. These processes generate grouped.csv, grouped_two.csv, pivot.csv, and top10.csv. They also participated in debugging and testing the program to 
ensure that the summaries were generated correctly from the processed records.


### Member 4 (NumPy Analysis and Visualization)
**Name: Arianne Denise Sumalinog**

**Github Username: ariannesumalinog**

Member 4 was responsible for the NumPy analysis and data visualization component. They developed analysis.py, which performs the NumPy array, Boolean mask, vectorized calculation, 
and loop-versus-NumPy comparison using five timing runs. The module also creates the required bar chart using top10.csv and the heatmap using pivot.csv, producing bar.png and heatmap.png. 
They also participated in debugging and testing the analysis and visualization components and their integration with the rest of the program.

### Member 5 (Validation and Documentation)
**Name: Olivia Patricia Jovita Baña**

**Github Username: olivia-bana**

Member 5 was responsible for validation and project documentation. They developed validation.py, which validates the dataset reference values, SHA-256 hash, filtering results, summary totals, 
plot source values, and agreement between the loop and vectorized calculations. The validation process generates validation.csv and audit_log.csv. Member 5 also worked on the project documentation, 
including the README and contribution records, and participated in debugging and testing the complete integrated program to verify that the required outputs were generated correctly.
