import pytest
from src.shared.decorators.query_reader import sql_query_reader
import os


def test_sql_query_reader_file_not_found(tmp_path):
    base_dir = tmp_path
    missing_file = "missing_query.sql"

    @sql_query_reader(base_dir, missing_file)
    def dummy_function():
        return True

    with pytest.raises(FileNotFoundError) as exc_info:
        dummy_function()

    expected_path = os.path.join(base_dir, "sql", missing_file)
    assert str(exc_info.value) == f"The file {expected_path} was not found"
