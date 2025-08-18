import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.src.processor.processor import Processor
from shapely.geometry import Polygon
import rasterio


@pytest.fixture
def processor_instance():
    return Processor(threshold=10000)


# --- read_band ---
@patch("rasterio.open")
def test_read_band_success(mock_open, processor_instance):
    mock_dataset = MagicMock()
    mock_dataset.read.return_value = np.array([[1, 2], [3, 4]])
    mock_dataset.profile = {"dtype": "uint16"}
    mock_open.return_value.__enter__.return_value = mock_dataset

    band, profile = processor_instance.read_band("dummy.tif")
    assert isinstance(band, np.ndarray)
    assert profile["dtype"] == "uint16"


# --- find_subfolder ---
@patch("pathlib.Path.rglob")
def test_find_subfolder_success(mock_rglob, processor_instance):
    mock_folder = MagicMock()
    mock_folder.is_dir.return_value = True
    mock_rglob.return_value = [mock_folder]

    result = processor_instance.find_subfolder("parent", "subfolder")
    assert result == mock_folder


def test_find_subfolder_none(processor_instance):
    result = processor_instance.find_subfolder("nonexistent", "subfolder")
    assert result is None


# --- clean_problematic_areas ---
def test_clean_problematic_areas(processor_instance):
    band = np.array([[5000, 15000], [8000, 12000]])
    cleaned = processor_instance.clean_problematic_areas(band)
    assert np.isnan(cleaned[0, 1])
    assert np.isnan(cleaned[1, 1])
    assert cleaned[0, 0] == 5000


# --- save_cleaned_band ---
@patch("rasterio.open")
def test_save_cleaned_band_success(mock_open, processor_instance):
    mock_dst = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_dst

    band = np.array([[1, np.nan], [3, 4]])
    profile = {"crs": None, "transform": MagicMock(), "height": 2, "width": 2}

    processor_instance.save_cleaned_band(band, profile, "output.tif")
    assert mock_dst.write.called


def test_save_cleaned_band_missing_transform(processor_instance):
    band = np.array([[1, 2], [3, 4]])
    profile = {"crs": None}  # Missing transform
    with pytest.raises(ValueError):
        processor_instance.save_cleaned_band(band, profile, "output.tif")


# --- visualize_band ---
@patch("rasterio.open")
@patch("matplotlib.pyplot.savefig")
def test_visualize_band_success(mock_savefig, mock_open, processor_instance):
    mock_src = MagicMock()
    mock_src.read.return_value = np.array([[1, 2], [3, 4]])
    mock_open.return_value.__enter__.return_value = mock_src

    processor_instance.visualize_band("image.tif", "output.png")
    assert mock_savefig.called


@patch("rasterio.open", side_effect=Exception("Simulated visualization error"))
def test_visualize_band_exception(mock_open, processor_instance):
    processor_instance.visualize_band("fake_image.tif", "output.png")


# --- extract_area_at_coordinates ---
@patch("rasterio.open")
@patch("rasterio.Env")
def test_extract_area_at_coordinates_success(mock_env, mock_open, processor_instance):
    mock_src = MagicMock()
    mock_src.read.return_value = np.array([[1, 2], [3, 4]])
    mock_src.profile = {
        "height": 2,
        "width": 2,
        "transform": MagicMock(),
        "crs": MagicMock(),
    }
    mock_src.window_transform.return_value = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_src

    processor_instance.extract_area_at_coordinates("image.tif", 0, 0, 2, "output.tif")
    assert mock_open.called


@patch("rasterio.open", side_effect=Exception("Simulated error"))
def test_extract_area_at_coordinates_exception(mock_open, processor_instance):
    processor_instance.extract_area_at_coordinates("image.tif", 0, 0, 2, "output.tif")


# --- generate_grid ---
def test_generate_grid_success():
    processor = Processor()
    polygon = Polygon(
        [
            (-75.0, 10.0),
            (-75.0, 10.001),
            (-74.999, 10.001),
            (-74.999, 10.0),
            (-75.0, 10.0),
        ]
    )
    grid_cells = processor.generate_grid(polygon)
    assert isinstance(grid_cells, list)
    assert all(isinstance(cell, Polygon) for cell in grid_cells)
    assert len(grid_cells) > 0


@patch("rasterio.Env")
@patch("rasterio.open")
@patch(
    "src.entities.machine_learning.src.processor.processor.rowcol",
    return_value=(50, 50),
)
def test_extract_area_at_coordinates_full(
    mock_rowcol, mock_open, mock_env, processor_instance
):
    mock_src = MagicMock()
    mock_src.transform = MagicMock()
    mock_src.read.return_value = np.ones((10, 10))
    mock_src.window_transform.return_value = MagicMock()
    mock_src.profile = {
        "height": 100,
        "width": 100,
        "transform": MagicMock(),
        "crs": MagicMock(),
        "driver": "GTiff",
        "dtype": "uint16",
        "count": 1,
        "nodata": 0,
    }

    mock_open.return_value.__enter__.return_value = mock_src

    processor_instance.extract_area_at_coordinates(
        image_path="dummy.tif", lon=0, lat=0, window_size=10, output_path="output.tif"
    )

    mock_rowcol.assert_called()


@patch("rasterio.open", side_effect=rasterio.errors.RasterioIOError("File not found"))
def test_visualize_band_rasterioioerror(mock_open, processor_instance):
    processor_instance.visualize_band("nonexistent.tif", "output.png")
