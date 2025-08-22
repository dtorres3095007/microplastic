import pytest
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.predictor import Predictor
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST

@pytest.fixture
def predictor():
    return Predictor(
        polygon="polygon_1",
        coordinates=[[[(-72.9, 11.5), (-72.8, 11.5), (-72.8, 11.6), (-72.9, 11.6), (-72.9, 11.5)]]],
        initial_date="2025-01-01",
        end_date="2025-01-31"
    )

def test_get_polygon_images_ok(predictor):
    with patch.object(predictor.integrations, "get_images", return_value=(STATUS_OK, "ok")) as mock_get, \
         patch.object(predictor.integrations, "clean_images", return_value=(STATUS_OK, "cleaned")) as mock_clean:
        status, msg = predictor.get_polygon_images()
    assert status == STATUS_OK
    assert msg == "cleaned"
    mock_get.assert_called_once()
    mock_clean.assert_called_once()

def test_create_polygons_ok(predictor):
    with patch.object(predictor.integrations, "create_polygons_10m", return_value=(STATUS_OK, "ok")) as mock_create:
        status, msg = predictor.create_polygons()
    assert status == STATUS_OK
    mock_create.assert_called_once()

def test_predict_ok(predictor):
    with patch("src.entities.machine_learning.predictor.Models") as mock_models:
        model_instance = mock_models.return_value
        model_instance.load_data.return_value = (STATUS_OK, MagicMock())
        model_instance.load_models.return_value = (STATUS_OK, "ok")
        model_instance.models = {
            "Linear Regression": MagicMock(),
            "Random Forest": MagicMock(),
            "Neural Network": MagicMock(),
        }
        model_instance.scaler.transform.return_value = MagicMock()
        for m in model_instance.models.values():
            m.predict.return_value = [0.5]
        status, msg = predictor.predict()
    assert status == STATUS_OK
    
def test_calculate_features_ok(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")):
        mock_listdir.side_effect = [
            ["img_folder"],         # os.listdir(base_dir)
            ["B01.tif", "B02.tif"] # os.listdir(image_path)
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndvi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndwi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndci.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_fdi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndpi.return_value = (STATUS_OK, "ok")
        status, msg = predictor.calculate_features()
    assert status == STATUS_OK
    assert "Features calculated" in msg["message"]

def test_calculate_features_fail_open_bands(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")), \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        mock_listdir.side_effect = [
            ["img_folder"],
            ["B01.tif", "B02.tif"]
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_BAD_REQUEST, "fail open_bands")
        predictor.calculate_features()
    mock_logger.error.assert_any_call("Error in open_bands: fail open_bands")


def test_calculate_features_fail_ndvi(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")), \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        mock_listdir.side_effect = [
            ["img_folder"],
            ["B01.tif", "B02.tif"]
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndvi.return_value = (STATUS_BAD_REQUEST, "fail ndvi")
        predictor.calculate_features()
    mock_logger.error.assert_any_call("Error in calculate_ndvi: fail ndvi")

def test_calculate_features_fail_ndwi(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")), \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        mock_listdir.side_effect = [
            ["img_folder"],
            ["B01.tif", "B02.tif"]
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndvi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndwi.return_value = (STATUS_BAD_REQUEST, "fail ndwi")
        predictor.calculate_features()
    mock_logger.error.assert_any_call("Error in calculate_ndwi: fail ndwi")

def test_calculate_features_fail_ndci(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")), \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        mock_listdir.side_effect = [
            ["img_folder"],
            ["B01.tif", "B02.tif"]
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndvi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndwi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndci.return_value = (STATUS_BAD_REQUEST, "fail ndci")
        predictor.calculate_features()
    mock_logger.error.assert_any_call("Error in calculate_ndci: fail ndci")

def test_calculate_features_fail_fdi(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")), \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        mock_listdir.side_effect = [
            ["img_folder"],
            ["B01.tif", "B02.tif"]
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndvi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndwi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndci.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_fdi.return_value = (STATUS_BAD_REQUEST, "fail fdi")
        predictor.calculate_features()
    mock_logger.error.assert_any_call("Error in calculate_fdi: fail fdi")

def test_calculate_features_fail_ndpi(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("src.entities.machine_learning.predictor.Feature") as mock_feature, \
         patch("os.path.splitext", side_effect=lambda f: (f.replace(".tif", ""), ".tif")), \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        mock_listdir.side_effect = [
            ["img_folder"],
            ["B01.tif", "B02.tif"]
        ]
        feature_instance = mock_feature.return_value
        feature_instance.open_bands.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndvi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndwi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndci.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_fdi.return_value = (STATUS_OK, "ok")
        feature_instance.calculate_ndpi.return_value = (STATUS_BAD_REQUEST, "fail ndpi")
        predictor.calculate_features()
    mock_logger.error.assert_any_call("Error in calculate_ndpi: fail ndpi")

def test_feature_mean_ok(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.makedirs"), \
         patch("os.listdir", return_value=["img_folder"]), \
         patch("os.path.exists", return_value=True), \
         patch("rasterio.open") as mock_rasterio, \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        # Simula un raster válido
        mock_src = MagicMock()
        mock_src.read.return_value = MagicMock()
        mock_src.read.return_value.astype.return_value = MagicMock()
        mock_src.nodata = 0
        mock_src.profile.copy.return_value = {"crs": "EPSG:4326", "dtype": "uint16"}
        mock_rasterio.return_value.__enter__.return_value = mock_src

        status, msg = predictor.feature_mean()
    assert status == STATUS_OK
    assert "Features mean saved" in msg["message"]
    mock_logger.info.assert_any_call("✅ Feature NDVI average calculated")

def test_bands_means_error(predictor):
    with patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
         patch("os.listdir") as mock_listdir, \
         patch("os.makedirs"), \
         patch("os.path.exists", return_value=True), \
         patch("rasterio.open") as mock_rasterio, \
         patch("src.entities.machine_learning.predictor.logger") as mock_logger:
        # Simula estructura de carpetas y archivos
        mock_listdir.side_effect = [
            ["img_folder"],         # os.listdir(base_dir)
            ["B01.tif", "B02.tif"] # os.listdir(folder_path)
        ]
        # Simula raster válido
        mock_src = MagicMock()
        mock_src.read.return_value = [[1, 2], [3, 4]]
        mock_src.nodata = 0
        mock_src.profile.copy.return_value = {"crs": "EPSG:4326", "dtype": "uint16"}
        mock_rasterio.return_value.__enter__.return_value = mock_src

        status, msg = predictor.bands_means()
    assert status == STATUS_BAD_REQUEST

def test_bands_means_error(predictor):
    with patch("os.listdir", side_effect=Exception("fail")):
        status, msg = predictor.bands_means()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

def test_clean_folders_ok(predictor):
    with patch("os.path.exists", return_value=True), \
         patch("shutil.rmtree") as mock_rmtree, \
         patch("os.makedirs") as mock_makedirs:
        status, msg = predictor.clean_folders()
    assert status == STATUS_OK
    assert "Folders cleaned" in msg["message"]
    mock_rmtree.assert_called_once()
    mock_makedirs.assert_called_once()

def test_create_polygons_ok(predictor):
    with patch.object(predictor.integrations, "create_polygons_10m", return_value=(STATUS_OK, "ok")) as mock_create:
        status, msg = predictor.create_polygons()
    assert status == STATUS_OK
    assert "Polygons created" in msg["message"]
    mock_create.assert_called_once()

def test_create_dataset_error(predictor):
    with patch("os.path.exists", return_value=True), \
         patch("os.makedirs"), \
         patch("os.listdir", return_value=["polygon_1"]), \
         patch("builtins.open", create=True), \
         patch("json.load") as mock_json_load, \
         patch("rasterio.open") as mock_rasterio, \
         patch("pandas.DataFrame.to_csv") as mock_to_csv:
        # Mock geojson data
        mock_json_load.return_value = {
            "features": [
                {"geometry": {"type": "Polygon", "coordinates": [[(-72.9, 11.5), (-72.8, 11.5), (-72.8, 11.6), (-72.9, 11.6), (-72.9, 11.5)]]}}
            ]
        }
        mock_dataset = MagicMock()
        mock_dataset.crs = "EPSG:4326"
        mock_dataset.read.return_value = [[1]]
        mock_dataset.nodata = 0
        mock_rasterio.return_value.__enter__.return_value = mock_dataset
        status, msg = predictor.create_dataset()
    assert "Dataset created" in msg["message"]
    mock_to_csv.assert_called_once()

def test_clean_folders_error(predictor):
    with patch("os.path.exists", side_effect=Exception("fail")), \
         patch("shutil.rmtree"), \
         patch("os.makedirs"):
        status, msg = predictor.clean_folders()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

def test_get_polygon_images_error_get(predictor):
    with patch.object(predictor.integrations, "get_images", return_value=(STATUS_BAD_REQUEST, "fail")) as mock_get:
        status, msg = predictor.get_polygon_images()
    assert status == STATUS_BAD_REQUEST
    assert msg == "fail"
    mock_get.assert_called_once()

def test_get_polygon_images_error_clean(predictor):
    with patch.object(predictor.integrations, "get_images", return_value=(STATUS_OK, "ok")), \
         patch.object(predictor.integrations, "clean_images", return_value=(STATUS_BAD_REQUEST, "fail")) as mock_clean:
        status, msg = predictor.get_polygon_images()
    assert status == STATUS_BAD_REQUEST
    assert msg == "fail"
    mock_clean.assert_called_once()

def test_calculate_features_error(predictor):
    with patch("os.listdir", side_effect=Exception("fail")):
        status, msg = predictor.calculate_features()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

def test_feature_mean_error(predictor):
    with patch("os.listdir", side_effect=Exception("fail")):
        status, msg = predictor.feature_mean()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

def test_create_polygons_error(predictor):
    with patch.object(predictor.integrations, "create_polygons_10m", side_effect=Exception("fail")):
        status, msg = predictor.create_polygons()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

def test_create_polygons_status_error(predictor):
    with patch.object(predictor.integrations, "create_polygons_10m", return_value=(STATUS_BAD_REQUEST, "fail")):
        status, msg = predictor.create_polygons()
    assert status == STATUS_BAD_REQUEST
    assert msg == "fail"

def test_create_dataset_error_open(predictor):
    with patch("builtins.open", side_effect=Exception("fail")):
        status, msg = predictor.create_dataset()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

def test_predict_error_load_data(predictor):
    with patch("src.entities.machine_learning.predictor.Models") as mock_models:
        model_instance = mock_models.return_value
        model_instance.load_data.return_value = (STATUS_BAD_REQUEST, "fail")
        status, msg = predictor.predict()
    assert status == STATUS_BAD_REQUEST
    assert msg == "fail"

def test_show_map_error(predictor):
    with patch("pandas.read_csv", side_effect=Exception("fail")):
        status, msg = predictor.show_map()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]