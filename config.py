from pathlib import Path

#files
file_path = Path("data/2015.csv")
output_path = Path("outputs")

#columns
req_cols = {"countryorigin_iso3", "tq", "dutiablevaluephp"}

#(category a) countryorigin_iso3 answers who since u cant analyze foreign trade without knowing where the goods came from.
#(category b) tq answers how. tq stands for tariff quota and quarter tracking. this categorizes hether shipments fall under specific import quotas, preferential trade agreements, or standard tariff rates.
#(provides the numbers for your team's summary tables and pivot reports) dutiablevaluephp answers how much. this is the primary numerical metric in the entire 500 MB dataset. itIt represents the taxable valuation of imported goods converted to philippine pesos.