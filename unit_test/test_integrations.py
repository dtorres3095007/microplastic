import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.src.integrations import Integrations
from src.shared.constants import STATUS_OK, STATUS_INTERNAL_SERVER_ERROR


@pytest.fixture
def folders(tmp_path):
    return {
        "MAIN": [str(tmp_path)],
        "ZIP": "zip",
        "EXTRACTED": "extracted",
        "CLEANED": "cleaned",
        "EXTRACTED_AREA": "area",
        "POLYGONS": "polygons"
    }


@pytest.fixture
def integrations(folders):
    return Integrations(folders)


def test_get_images_ok(integrations, tmp_path):
    mock_results = {
        "value": [
            {"GeoFootprint": {"type": "Polygon", "coordinates": []},
             "Name": "TILE_L2A.SAFE",
             "Id": "123"}
        ]
    }

    mock_copernicus = MagicMock()
    mock_copernicus.search.return_value = mock_results
    mock_copernicus.extract_zip.return_value = (STATUS_OK, "ok")

    with patch.object(integrations, "copernicus", return_value=mock_copernicus), \
         patch("src.entities.machine_learning.src.integrations.gpd.GeoDataFrame") as mock_gdf:
        mock_gdf.return_value.set_geometry.return_value = pd.DataFrame([{
            "Name": "TILE_L2A.SAFE",
            "Id": "123",
            "geometry": MagicMock()
        }])

        status, msg = integrations.get_images("polygon", "2020-01-01", "2020-12-31")

    assert status == STATUS_OK
    assert "Images downloaded" in msg["message"]


def test_get_images_no_results(integrations):
    mock_copernicus = MagicMock()
    mock_copernicus.search.return_value = None

    with patch.object(integrations, "copernicus", return_value=mock_copernicus):
        status, msg = integrations.get_images("polygon", "2020", "2021")

    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "Error in search" in msg["message"]


def test_clean_images_ok(integrations, tmp_path):
    subfolder = tmp_path / "extracted" / "sub"
    os.makedirs(subfolder, exist_ok=True)

    processor = MagicMock()
    processor.find_subfolder.return_value = str(subfolder)
    processor.read_band.return_value = ("band", {"profile": 1})
    processor.clean_problematic_areas.return_value = "cleaned_band"
    processor.rescale_band.return_value = ("rescaled_band", {"profile": 1})

    with patch.object(integrations, "processor", return_value=processor), \
         patch("src.entities.machine_learning.src.integrations.get_band_name", return_value="B01"), \
         patch("os.listdir", return_value=["img.jp2"]):
        status, msg = integrations.clean_images()

    assert status == STATUS_OK
    assert "Images cleaned" in msg["message"]


def test_clean_images_exception(integrations):
    with patch.object(integrations, "processor", side_effect=Exception("fail")):
        status, msg = integrations.clean_images()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "An error occurred" in msg["message"]


def test_visualize_images_ok(integrations, tmp_path):
    subfolder = tmp_path / "cleaned" / "sub"
    os.makedirs(subfolder, exist_ok=True)
    tif_file = subfolder / "img.tif"
    tif_file.write_text("dummy")

    processor = MagicMock()

    with patch.object(integrations, "processor", return_value=processor):
        status, msg = integrations.visualize_images(str(tmp_path), str(tmp_path / "out"))

    assert status == STATUS_OK
    assert "visualized" in msg["message"]


def test_visualize_images_exception(integrations):
    with patch.object(integrations, "processor", side_effect=Exception("boom")):
        status, msg = integrations.visualize_images("in", "out")
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "An error occurred" in msg["message"]


def test_create_polygons_ok(integrations, tmp_path):
    processor = MagicMock()
    processor.generate_grid.return_value = [MagicMock()]

    with patch.object(integrations, "processor", return_value=processor), \
         patch("src.entities.machine_learning.src.integrations.gpd.GeoDataFrame") as mock_gdf:
        mock_gdf.return_value.to_file.return_value = None
        status, msg = integrations.create_polygons_10m([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

    assert status == STATUS_OK
    assert "Polygons created" in msg["message"]


def test_create_polygons_exception(integrations):
    with patch.object(integrations, "processor", side_effect=Exception("fail")):
        status, msg = integrations.create_polygons_10m([[0, 0], [1, 0]])
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "create_polygons_10m" in msg["message"]
