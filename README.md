# MP1 Data Pipeline

This project is a command-line data pipeline that loads a dataset, validates it, cleans it, and saves the result, with all cleaning behavior controlled by `config/config.yaml` instead of hard-coded values. `pipeline.py` coordinates the run: it parses the command-line arguments, checks that the input and config files exist, and calls each stage in order. Data moves from loading, to validation, to processing, to output. `src/data_loaders.py` reads CSV, JSON, and YAML files, and `src/data_validator.py` checks that required columns exist and removes rows whose numeric columns contain values that can't be converted to numbers. `src/data_processor.py` removes duplicate rows, handles missing values, removes outliers using the IQR or z-score method, and builds the cleaning report. `src/data_output.py` saves the cleaned data as a CSV and creates the output folder if needed, while `src/utils.py` holds the shared logging setup and file-path validation. Because the settings live in the config file, the pipeline can process a different compatible dataset by changing only the command-line paths and the column names in the config.

## Example
```
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:
```
20:34:37 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
20:34:37 INFO     src.utils — Input file validated: fixtures/sample_data.csv
20:34:37 INFO     src.utils — Input file validated: config/config.yaml
20:34:37 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
20:34:37 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
20:34:37 WARNING  src.data_validator — Invalid numeric value in rating at row 94: 'not_available'
20:34:37 WARNING  src.data_validator — Invalid numeric value in rating at row 95: 'error'
20:34:37 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
20:34:37 DEBUG    src.data_validator — Validation: 100 -> 98 rows (2 removed)
20:34:37 INFO     __main__ — Validation complete: 100 -> 98 rows
20:34:37 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
20:34:37 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
20:34:37 DEBUG    src.data_processor — remove_outliers: method=iqr, threshold=1.5
20:34:37 DEBUG    src.data_processor — rating: lower=43.625, upper=106.625, removed=2
20:34:37 INFO     __main__ — Processing complete: 98 -> 92 rows
20:34:37 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
20:34:37 INFO     __main__ — Saved cleaned data to output\clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```