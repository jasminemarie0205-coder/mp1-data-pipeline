import logging
import pandas as pd
logger = logging.getLogger(__name__)
def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    logger.debug("remove_duplicates: %d → %d rows", before, len(df))
    return df
    
def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        before = len(df)
        df = df.dropna(axis=0)
        logger.debug("handle_missing: %d → %d rows", before, len(df))
    elif axis == "columns":
        before = len(df.columns)
        df = df.dropna(axis=1)
        logger.debug("handle_missing: %d → %d columns", before, len(df.columns))
    else:
        logger.error("Unsupported axis: %s", axis)
        raise ValueError(f"Unsupported axis: {axis}")
    return df

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ("iqr", "zscore"):
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    logger.debug("remove_outliers: method=%s, threshold=%s", method, threshold)

    for col in columns:
        if col not in df.columns:
            logger.warning("Column not found: %s", col)
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column is not numeric: %s", col)
            continue

        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
        else:  
            mean = df[col].mean()
            std = df[col].std()
            lower = mean - threshold * std
            upper = mean + threshold * std

        if pd.isna(lower) or pd.isna(upper):
            logger.warning("Not enough data to compute bounds for column: %s", col)
            continue

        before = len(df)
        mask = df[col].between(lower, upper) | df[col].isna()
        df = df[mask]
        logger.debug("%s: lower=%s, upper=%s, removed=%d",
                    col, lower, upper, before - len(df))
    return df

def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]

    
    if settings.get("remove_duplicates", False):
        df = remove_duplicates(df)

    
    missing = settings.get("missing", {})
    if missing.get("enabled", False):
        df = handle_missing(df, axis=missing["axis"])

    
    outliers = settings.get("outliers", {})
    if outliers.get("enabled", False):
        df = remove_outliers(
            df,
            columns=outliers["columns"],
            method=outliers["method"],
            threshold=outliers["threshold"],
        )

    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    rows_before, columns_before = df_before.shape
    rows_after, columns_after = df_after.shape
    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_before - rows_after,
        "columns_before": columns_before,
        "columns_after": columns_after,
        "columns_removed": columns_before - columns_after,
    }