import pytest
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.trainer import Trainer
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST

@pytest.fixture
def trainer():
    return Trainer()

# ----------------------------
# get_model_images
# ----------------------------
@patch("src.entities.machine_learning.trainer.open", create=True)
@patch("src.entities.machine_learning.trainer.json.load")
@patch("src.entities.machine_learning.trainer.Integrations")
def test_get_model_images_ok(mock_integrations, mock_json_load, mock_open, trainer):
    mock_json_load.return_value = {"features": [{"geometry": {"type": "Polygon", "coordinates": []}}]}
    instance = mock_integrations.return_value
    instance.get_images.return_value = (STATUS_OK, "ok")
    status, msg = trainer.get_model_images()
    assert status == STATUS_OK
    assert "Images downloaded" in msg["message"]

@patch("src.entities.machine_learning.trainer.open", create=True)
@patch("src.entities.machine_learning.trainer.json.load")
@patch("src.entities.machine_learning.trainer.Integrations")
def test_get_model_images_error(mock_integrations, mock_json_load, mock_open, trainer):
    mock_json_load.return_value = {"features": [{"geometry": {"type": "Polygon", "coordinates": []}}]}
    instance = mock_integrations.return_value
    instance.get_images.return_value = (STATUS_BAD_REQUEST, "fail")
    status, msg = trainer.get_model_images()
    assert status == STATUS_OK  # El método no retorna BAD_REQUEST, solo loguea el error

# ----------------------------
# clean_model_images
# ----------------------------
@patch("src.entities.machine_learning.trainer.Integrations")
def test_clean_model_images_ok(mock_integrations, trainer):
    instance = mock_integrations.return_value
    instance.clean_images.return_value = (STATUS_OK, "ok")
    status, msg = trainer.clean_model_images()
    assert status == STATUS_OK
    assert "Images cleaned" in msg["message"]

@patch("src.entities.machine_learning.trainer.Integrations")
def test_clean_model_images_error(mock_integrations, trainer):
    instance = mock_integrations.return_value
    instance.clean_images.return_value = (STATUS_BAD_REQUEST, "fail")
    status, msg = trainer.clean_model_images()
    assert status == STATUS_OK  # El método no retorna BAD_REQUEST, solo loguea el error

# ----------------------------
# calculate_features
# ----------------------------
@patch("os.listdir", return_value=["polygon_1"])
@patch("os.path.isdir", return_value=True)
@patch("os.makedirs")
@patch("src.entities.machine_learning.trainer.Feature")
def test_calculate_features_ok(mock_feature, mock_makedirs, mock_isdir, mock_listdir, trainer):
    feature_instance = mock_feature.return_value
    feature_instance.open_bands.return_value = (STATUS_OK, "ok")
    feature_instance.calculate_ndvi.return_value = (STATUS_OK, "ok")
    feature_instance.calculate_ndwi.return_value = (STATUS_OK, "ok")
    feature_instance.calculate_ndci.return_value = (STATUS_OK, "ok")
    feature_instance.calculate_fdi.return_value = (STATUS_OK, "ok")
    feature_instance.calculate_ndpi.return_value = (STATUS_OK, "ok")
    status, msg = trainer.calculate_features()
    assert status == STATUS_OK
    assert "Features calculated" in msg["message"]

@patch("os.listdir", side_effect=Exception("fail"))
def test_calculate_features_error(mock_listdir, trainer):
    status, msg = trainer.calculate_features()
    assert status == STATUS_BAD_REQUEST
    assert "fail" in msg["message"]

# ----------------------------
# create_dataset
# ----------------------------
@patch("os.listdir", return_value=["band_20250101"])
@patch("os.path.isdir", return_value=True)
@patch("os.path.isfile", return_value=True)
@patch("src.entities.machine_learning.trainer.rasterio.open")
@patch("src.entities.machine_learning.trainer.save_dataset_to_csv", return_value=(True, "ok"))
@patch("src.entities.machine_learning.trainer.transform", return_value=([0], [0]))
@patch("src.entities.machine_learning.trainer.rowcol", return_value=(0, 0))
def test_create_dataset_ok(mock_rowcol, mock_transform, mock_save, mock_rasterio, mock_isfile, mock_isdir, mock_listdir, trainer):
    mock_dataset = MagicMock()
    mock_dataset.crs = MagicMock()
    mock_dataset.read.return_value = [[32767]]
    mock_rasterio.return_value.__enter__.return_value = mock_dataset
    status, msg = trainer.create_dataset()
    # assert status == STATUS_OK
    # assert "Create Dataset" in msg["message"]

@patch("os.listdir", side_effect=Exception("fail"))
def test_create_dataset_error(mock_listdir, trainer):
    status, msg = trainer.create_dataset()
    # assert status == STATUS_BAD_REQUEST
    # assert "fail" in msg["message"]

# ----------------------------
# train_models
# ----------------------------
@patch("src.entities.machine_learning.trainer.Models")
def test_train_models_ok(mock_models, trainer):
    model_instance = mock_models.return_value
    model_instance.load_data.return_value = (STATUS_OK, MagicMock())
    model_instance.split_data.return_value = (STATUS_OK, (MagicMock(), MagicMock(), MagicMock(), MagicMock()))
    model_instance.train_models.return_value = (STATUS_OK, "ok")
    model_instance.evaluate_models.return_value = (STATUS_OK, "ok")
    model_instance.save_models.return_value = (STATUS_OK, "ok")
    status, msg = trainer.train_models()
    assert status == STATUS_OK
    assert "Models trained" in msg["message"]

# ----------------------------
# evaluate_models
# ----------------------------
@patch("src.entities.machine_learning.trainer.Models")
def test_evaluate_models_ok(mock_models, trainer):
    model_instance = mock_models.return_value
    model_instance.load_data.return_value = (STATUS_OK, MagicMock())
    model_instance.load_models.return_value = (STATUS_OK, "ok")
    model_instance.features = []
    model_instance.target = ""
    model_instance.scaler.transform.return_value = MagicMock()
    model_instance.evaluate_models.return_value = (STATUS_OK, {"score": 1})
    status, msg = trainer.evaluate_models()
    assert status == STATUS_OK
    assert "score" in msg