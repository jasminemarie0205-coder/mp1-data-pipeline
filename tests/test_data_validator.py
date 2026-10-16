# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    required_columns = ["record_id", "name", "rating", "category", "status"]
    numeric_columns = ["rating"]

    result = validate_dataframe(sample_df, required_columns, numeric_columns)

    assert len(result) == 98
    assert list(result.columns) == required_columns


def test_validate_dataframe_with_missing_column(sample_df):
    required_columns = ["record_id", "name", "rating", "category", "status", "price"]
    numeric_columns = ["rating"]

    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns, numeric_columns)