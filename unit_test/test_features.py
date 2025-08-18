import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.src.features.features import Feature
from src.shared.constants import (
    STATUS_OK,
    STATUS_BAD_REQUEST,
    STATUS_INTERNAL_SERVER_ERROR,
)


@pytest.fixture
def feature_instance(tmp_path):
    path_bands = {
        "RED": "red.tif",
        "GREEN": "green.tif",
        "NIR_10m": "nir.tif",
        "SWIR1": "swir.tif",
        "REDEDGE1": "rededge.tif",
    }
    return Feature(path_bands, tmp_path)


# ----------------------------
# Test open_bands
# ----------------------------
@patch("rasterio.open")
def test_open_bands_success(mock_rasterio_open, feature_instance):
    mock_src = MagicMock()
    mock_src.read.return_value = np.ones((1, 5, 5))
    mock_rasterio_open.return_value.__enter__.return_value = mock_src

    status, msg = feature_instance.open_bands()

    assert status == STATUS_OK
    for band in ["RED", "GREEN", "NIR_10m", "SWIR1", "REDEDGE1"]:
        assert band in feature_instance.bands


@patch("rasterio.open", side_effect=Exception("Fail to open"))
def test_open_bands_failure(mock_rasterio_open, feature_instance):
    status, msg = feature_instance.open_bands()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error opening band" in msg


def test_calculate_ndvi_success(feature_instance):
    feature_instance.bands = {
        "RED": np.array([[1, 2], [3, 4]], dtype=np.float32),
        "NIR_10m": np.array([[2, 3], [4, 5]], dtype=np.float32),
    }
    with patch.object(feature_instance, "save_feature", return_value=(STATUS_OK, {})):
        status, msg = feature_instance.calculate_ndvi()
    assert status == STATUS_OK


def test_calculate_ndvi_missing_band(feature_instance):
    feature_instance.bands = {"RED": np.array([[1]])}
    status, msg = feature_instance.calculate_ndvi()
    assert status == STATUS_BAD_REQUEST


# NDWI
def test_calculate_ndwi_success(feature_instance):
    feature_instance.bands = {
        "GREEN": np.array([[1, 2]]),
        "NIR_10m": np.array([[2, 3]]),
    }
    with patch.object(feature_instance, "save_feature", return_value=(STATUS_OK, {})):
        status, msg = feature_instance.calculate_ndwi()
    assert status == STATUS_OK


# NDCI
def test_calculate_ndci_success(feature_instance):
    feature_instance.bands = {
        "REDEDGE1": np.array([[2]]),
        "RED": np.array([[1]]),
    }
    with patch.object(feature_instance, "save_feature", return_value=(STATUS_OK, {})):
        status, msg = feature_instance.calculate_ndci()
    assert status == STATUS_OK


# FDI
def test_calculate_fdi_success(feature_instance):
    feature_instance.bands = {
        "SWIR1": np.array([[3]]),
        "NIR_10m": np.array([[1]]),
    }
    with patch.object(feature_instance, "save_feature", return_value=(STATUS_OK, {})):
        status, msg = feature_instance.calculate_fdi()
    assert status == STATUS_OK


# NDPI
def test_calculate_ndpi_success(feature_instance):
    feature_instance.bands = {
        "RED": np.array([[2]]),
        "SWIR1": np.array([[1]]),
    }
    with patch.object(feature_instance, "save_feature", return_value=(STATUS_OK, {})):
        status, msg = feature_instance.calculate_ndpi()
    assert status == STATUS_OK


@patch("rasterio.open", side_effect=Exception("Can't open"))
def test_save_feature_error(mock_rasterio_open, feature_instance):
    arr = np.array([[1]])
    status, msg = feature_instance.save_feature(arr, "file.tif")
    assert status == STATUS_INTERNAL_SERVER_ERROR


def test_calculate_ndvi_exception(feature_instance):
    feature_instance.bands = {"RED": np.array([[1]]), "NIR_10m": np.array([[2]])}
    with patch.object(
        feature_instance, "save_feature", side_effect=Exception("NDVI error")
    ):
        status, msg = feature_instance.calculate_ndvi()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in NDVI" in msg["message"]


@patch("rasterio.open")
def test_save_feature_success(mock_rasterio_open, feature_instance, tmp_path):
    mock_src = MagicMock()
    mock_src.profile = {
        "dtype": "float32",
        "count": 1,
        "driver": "GTiff",
        "crs": "EPSG:4326",
    }
    mock_rasterio_open.return_value.__enter__.return_value = mock_src

    arr = np.array([[0.5]], dtype=np.float32)
    status, msg = feature_instance.save_feature(arr, "test_output.tif")
    assert status == STATUS_OK
    assert "Feature test_output.tif saved." in msg["message"]


@patch("rasterio.open")
def test_open_bands_skips_unused_band(mock_rasterio_open, tmp_path):
    path_bands = {
        "RED": "red.tif",
        "GREEN": "green.tif",
        "NIR_10m": "nir.tif",
        "SWIR1": "swir.tif",
        "REDEDGE1": "rededge.tif",
        "UNUSED_BAND": "unused.tif",
    }
    feature = Feature(path_bands, tmp_path)

    mock_src = MagicMock()
    mock_src.read.return_value = np.ones((1, 5, 5))
    mock_rasterio_open.return_value.__enter__.return_value = mock_src
    status, msg = feature.open_bands()

    assert status == STATUS_OK
    assert "UNUSED_BAND" not in feature.bands


def test_calculate_ndwi_missing_both_bands(feature_instance):
    feature_instance.bands = {}
    status, msg = feature_instance.calculate_ndwi()
    assert status == STATUS_BAD_REQUEST


def test_calculate_ndwi_exception(feature_instance):
    feature_instance.bands = {"GREEN": np.array([[1.0]]), "NIR_10m": np.array([[2.0]])}
    with patch.object(
        feature_instance, "save_feature", side_effect=Exception("NDWI error")
    ):
        status, msg = feature_instance.calculate_ndwi()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in NDWI" in msg["message"]


def test_calculate_ndwi_exception(feature_instance):
    feature_instance.bands = {"GREEN": np.array([[1.0]]), "NIR_10m": np.array([[2.0]])}
    with patch.object(
        feature_instance, "save_feature", side_effect=Exception("NDWI error")
    ):
        status, msg = feature_instance.calculate_ndwi()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in NDWI" in msg["message"]


def test_calculate_ndci_exception(feature_instance):
    feature_instance.bands = {"REDEDGE1": np.array([[2.0]]), "RED": np.array([[1.0]])}
    with patch.object(
        feature_instance, "save_feature", side_effect=Exception("NDCI error")
    ):
        status, msg = feature_instance.calculate_ndci()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in NDCI" in msg["message"]


def test_calculate_fdi_missing_band(feature_instance):
    feature_instance.bands = {"SWIR1": np.array([[1.0]])}
    status, msg = feature_instance.calculate_fdi()
    assert status == STATUS_BAD_REQUEST
    assert "Missing required bands for FDI." in msg["message"]


def test_calculate_fdi_exception(feature_instance):
    feature_instance.bands = {"SWIR1": np.array([[3.0]]), "NIR_10m": np.array([[1.0]])}
    with patch.object(
        feature_instance, "save_feature", side_effect=Exception("FDI error")
    ):
        status, msg = feature_instance.calculate_fdi()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in FDI" in msg["message"]


def test_calculate_ndpi_missing_band(feature_instance):
    feature_instance.bands = {"RED": np.array([[1.0]])}
    status, msg = feature_instance.calculate_ndpi()
    assert status == STATUS_BAD_REQUEST
    assert "Missing required bands for NDPI." in msg["message"]


def test_calculate_ndpi_exception(feature_instance):
    feature_instance.bands = {"RED": np.array([[2.0]]), "SWIR1": np.array([[1.0]])}
    with patch.object(
        feature_instance, "save_feature", side_effect=Exception("NDPI error")
    ):
        status, msg = feature_instance.calculate_ndpi()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in NDPI" in msg["message"]


def test_calculate_ndci_missing_band(feature_instance):
    feature_instance.bands = {"RED": np.array([[1.0]])}
    status, msg = feature_instance.calculate_ndci()
    assert status == STATUS_BAD_REQUEST
    assert "Missing required bands for NDCI." in msg["message"]
