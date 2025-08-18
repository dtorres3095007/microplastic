import pytest
import os
import pandas as pd
from src.shared.utils import get_band_name, save_dataset_to_csv


# --- get_band_name ---
def test_get_band_name_existing():
    filename = "LC08_L1TP_123045_20210101_20210101_01_T1_B4_.tif"
    band_name = get_band_name(filename)
    assert band_name is not None


def test_get_band_name_nonexistent_band():
    filename = "LC08_L1TP_123045_20210101_20210101_01_T1_B99_.tif"
    band_name = get_band_name(filename)
    assert band_name == "B99"


def test_get_band_name_no_match():
    filename = "LC08_L1TP_123045_20210101_20210101_01_T1_.tif"
    band_name = get_band_name(filename)
    assert band_name is None


# --- save_dataset_to_csv ---
def test_save_dataset_to_csv_success(tmp_path):
    data = [{"col1": 1, "col2": 2}, {"col1": 3, "col2": 4}]
    folder = tmp_path / "datasets"
    success, message = save_dataset_to_csv(
        data, folder=str(folder), file_name="testfile"
    )

    assert success
    file_path = folder / "testfile.csv"
    assert os.path.exists(file_path)

    df = pd.read_csv(file_path)
    assert df.shape[0] == 2
    assert df.shape[1] == 2


def test_save_dataset_to_csv_exception(monkeypatch, tmp_path):
    data = [{"col1": 1, "col2": 2}]

    def mock_makedirs(*args, **kwargs):
        raise OSError("Cannot create directory")

    monkeypatch.setattr("os.makedirs", mock_makedirs)

    success, message = save_dataset_to_csv(
        data, folder=str(tmp_path / "datasets"), file_name="testfile"
    )
    assert not success
    assert "Cannot create directory" in message
