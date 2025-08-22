import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.src.models.models import Models
from src.shared.constants import (
    STATUS_OK,
    STATUS_BAD_REQUEST,
    FEATURE_NDVI,
    FEATURE_NDWI,
    FEATURE_NDCI,
    FEATURE_FDI,
    FEATURE_NDPI,
    BAND_SWIR1,
    BAND_SWIR2
)


@pytest.fixture
def sample_dataframe():
    data = {
        FEATURE_NDVI: np.random.rand(100),
        FEATURE_NDWI: np.random.rand(100),
        FEATURE_NDCI: np.random.rand(100),
        FEATURE_FDI: np.random.rand(100),
        FEATURE_NDPI: np.random.rand(100),
        BAND_SWIR1: np.random.rand(100),
        BAND_SWIR2: np.random.rand(100),
        "microplastic_concentration": np.random.rand(100),
    }
    return pd.DataFrame(data)


@pytest.fixture
def models_instance(tmp_path):
    return Models(csv_path="dummy.csv", models_path=str(tmp_path))


# --- load_data ---
@patch("pandas.read_csv")
def test_load_data_success(mock_read_csv, models_instance, sample_dataframe):
    mock_read_csv.return_value = sample_dataframe
    status, df = models_instance.load_data()
    assert status == STATUS_OK
    assert isinstance(df, pd.DataFrame)


@patch("pandas.read_csv", side_effect=Exception("File error"))
def test_load_data_failure(mock_read_csv, models_instance):
    status, msg = models_instance.load_data()
    assert status == STATUS_BAD_REQUEST
    assert "message" in msg


# --- split_data ---
def test_split_data_success(models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    print("errorr ------", data)
    assert status == STATUS_OK
    X_train, X_test, y_train, y_test = data
    assert len(X_train) > 0 and len(X_test) > 0


def test_split_data_failure(models_instance):
    df = pd.DataFrame({"invalid_column": [1, 2, 3]})
    status, msg = models_instance.split_data(df)
    assert status == STATUS_BAD_REQUEST


# --- train_models ---
def test_train_models_success(models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    X_train, _, y_train, _ = data
    status, msg = models_instance.train_models(X_train, y_train)
    assert status == STATUS_OK
    assert "Linear Regression" in models_instance.models


# --- evaluate_models ---
def test_evaluate_models_success(models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    X_train, X_test, y_train, y_test = data
    models_instance.train_models(X_train, y_train)
    status, results = models_instance.evaluate_models(X_test, y_test)
    assert status == STATUS_OK
    assert "Linear Regression" in results


# --- save_models ---
@patch("joblib.dump")
def test_save_models_success(mock_dump, models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    X_train, _, y_train, _ = data
    models_instance.train_models(X_train, y_train)
    status, msg = models_instance.save_models()
    assert status == STATUS_OK


# --- load_models ---
@patch("joblib.load")
def test_load_models_success(mock_load, models_instance):
    mock_model = MagicMock()
    mock_load.return_value = mock_model
    status, msg = models_instance.load_models()
    assert status == STATUS_OK


@patch("src.entities.machine_learning.src.models.models.LinearRegression")
def test_train_models_exception(mock_lr, models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    X_train, _, y_train, _ = data

    # Simular error en el método fit
    mock_model = MagicMock()
    mock_model.fit.side_effect = Exception("Training error")
    mock_lr.return_value = mock_model

    status, msg = models_instance.train_models(X_train, y_train)
    assert status == STATUS_BAD_REQUEST
    assert "message" in msg


def test_evaluate_models_exception(models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    X_train, X_test, y_train, y_test = data
    models_instance.train_models(X_train, y_train)

    # Simular error con datos mal formateados
    X_test_faulty = X_test[:, :-1]  # Quitar una columna

    status, msg = models_instance.evaluate_models(X_test_faulty, y_test)
    assert status == STATUS_BAD_REQUEST
    assert "message" in msg


@patch("joblib.dump", side_effect=Exception("Save error"))
def test_save_models_exception(mock_dump, models_instance, sample_dataframe):
    status, data = models_instance.split_data(sample_dataframe)
    X_train, _, y_train, _ = data
    models_instance.train_models(X_train, y_train)

    status, msg = models_instance.save_models()
    assert status == STATUS_BAD_REQUEST
    assert "message" in msg


@patch("joblib.load", side_effect=Exception("Load error"))
def test_load_models_exception(mock_load, models_instance):
    status, msg = models_instance.load_models()
    assert status == STATUS_BAD_REQUEST
    assert "message" in msg
