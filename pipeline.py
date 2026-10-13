"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)





def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Path to input file")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to output file")
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()





def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}")

    # validate file paths
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # load data and config
    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # read validation settings from the config
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # validate the data
    rows_loaded = len(df)
    try:
        df = validate_dataframe(df, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d -> %d rows", rows_loaded, len(df))

    df_original = df.copy()
    try:
        df_clean = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df_clean)
    logger.info("Processing complete: %d -> %d rows",
                report["rows_before"], report["rows_after"])

    #  save with save_data()
    output_path = save_data(df_clean, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    
    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()