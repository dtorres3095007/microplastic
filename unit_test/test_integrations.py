import pytest
from unittest.mock import patch
from src.entities.machine_learning.src.integrations import Integrations
from src.shared.constants import STATUS_OK, STATUS_INTERNAL_SERVER_ERROR


@pytest.fixture
def integrations_instance(tmp_path, monkeypatch):
    folders = {
        "MAIN": ["test_main"],
        "ZIP": "zip_folder",
        "EXTRACTED": "extracted",
        "CLEANED": "cleaned",
        "EXTRACTED_AREA": "extracted_area",
        "POLYGONS": "polygons",
    }
    monkeypatch.chdir(tmp_path)
    return Integrations(folders)


@patch("src.entities.machine_learning.src.integrations.Copernicus")
def test_get_images_search_fail(mock_copernicus, integrations_instance):
    mock_cop = mock_copernicus.return_value
    mock_cop.search.return_value = None
    status, msg = integrations_instance.get_images(
        "POLYGON((...))", "2023-01-01", "2023-01-31"
    )
    assert status == STATUS_INTERNAL_SERVER_ERROR


# ----------------------------
# Test clean_images
# ----------------------------
@patch("os.listdir")
@patch("os.makedirs")
@patch("src.entities.machine_learning.src.integrations.Processor")
def test_clean_images_success(
    mock_processor_class, mock_makedirs, mock_listdir, integrations_instance, tmp_path
):
    mock_listdir.return_value = ["tile1"]
    mock_processor = mock_processor_class.return_value
    mock_processor.find_subfolder.return_value = tmp_path / "tile1"
    mock_processor.read_band.return_value = ([1], {"profile": 1})
    mock_processor.clean_problematic_areas.return_value = [1]
    mock_processor.rescale_band.return_value = ([1], {"profile": 1})
    mock_processor.save_cleaned_band.return_value = None

    status, msg = integrations_instance.clean_images()
    assert status == STATUS_OK


# ----------------------------
# Test visualize_images
# ----------------------------
@patch("os.listdir")
@patch("os.makedirs")
@patch("src.entities.machine_learning.src.integrations.Processor")
def test_visualize_images_success(
    mock_processor_class, mock_makedirs, mock_listdir, integrations_instance, tmp_path
):
    mock_listdir.return_value = ["tile1"]
    mock_processor = mock_processor_class.return_value
    mock_processor.visualize_band.return_value = None

    input_dir = tmp_path / "cleaned"
    input_dir.mkdir()
    subfolder = input_dir / "tile1"
    subfolder.mkdir()
    (subfolder / "B04.tif").write_text("fake data")

    status, msg = integrations_instance.visualize_images(
        str(input_dir), str(tmp_path / "output")
    )
    assert status == STATUS_OK


# ----------------------------
# Test extract_area_at_coordinates
# ----------------------------
@patch("os.listdir")
@patch("os.makedirs")
@patch("src.entities.machine_learning.src.integrations.Processor")
def test_extract_area_at_coordinates_success(
    mock_processor_class, mock_makedirs, mock_listdir, integrations_instance, tmp_path
):
    mock_listdir.return_value = ["tile1"]
    mock_processor = mock_processor_class.return_value
    mock_processor.extract_area_at_coordinates.return_value = None

    status, msg = integrations_instance.extract_area_at_coordinates(0, 0, 10)
    assert status == STATUS_OK


@patch("src.entities.machine_learning.src.integrations.Processor")
def test_clean_images_exception(mock_processor_class, integrations_instance):
    mock_processor = mock_processor_class.return_value
    mock_processor.find_subfolder.side_effect = Exception("Simulated error")
    status, msg = integrations_instance.clean_images()
    assert status == STATUS_INTERNAL_SERVER_ERROR
    assert "message" in msg


@patch("os.listdir")
@patch("os.makedirs")
@patch("src.entities.machine_learning.src.integrations.Processor")
def test_clean_images_with_invalid_band(
    mock_processor_class, mock_makedirs, mock_listdir, integrations_instance, tmp_path
):
    mock_listdir.return_value = ["tile1"]
    mock_processor = mock_processor_class.return_value
    mock_processor.find_subfolder.return_value = tmp_path / "tile1"
    mock_processor.read_band.return_value = ([1], {"profile": 1})
    mock_processor.clean_problematic_areas.return_value = [1]
    mock_processor.rescale_band.return_value = ([1], {"profile": 1})
    mock_processor.save_cleaned_band.return_value = None

    with patch("os.listdir", return_value=["B99.jp2"]):
        status, msg = integrations_instance.clean_images()
        assert status == STATUS_OK
