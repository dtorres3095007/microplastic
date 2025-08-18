import pytest
import os
from unittest.mock import patch, MagicMock
from src.entities.machine_learning.src.copernicus.copernicus import Copernicus
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST


@pytest.fixture
def copernicus_instance():
    return Copernicus()


### 1. authenticate success
@patch("requests.post")
def test_authenticate_success(mock_post, copernicus_instance):
    mock_post.return_value.status_code = STATUS_OK
    mock_post.return_value.json.return_value = {"access_token": "fake-token"}

    token = copernicus_instance.authenticate()

    assert token == "fake-token"
    mock_post.assert_called_once()


### 2. authenticate failure
@patch("requests.post")
def test_authenticate_failure(mock_post, copernicus_instance):
    mock_post.side_effect = Exception("Network error")

    with pytest.raises(Exception) as exc:
        copernicus_instance.authenticate()

    assert "authenticate token creation failed" in str(exc.value)


### 3. search success
@patch("requests.get")
def test_search_success(mock_get, copernicus_instance):
    mock_get.return_value.status_code = STATUS_OK
    mock_get.return_value.json.return_value = {"results": []}

    result = copernicus_instance.search("POLYGON((...))", "2023-01-01", "2023-01-31")

    assert result == {"results": []}
    mock_get.assert_called_once()


### 4. search failure
@patch("requests.get")
def test_search_failure(mock_get, copernicus_instance):
    mock_get.return_value.status_code = STATUS_BAD_REQUEST

    result = copernicus_instance.search("POLYGON((...))", "2023-01-01", "2023-01-31")

    assert result is None


### 5. extract_zip success
@patch("zipfile.ZipFile")
def test_extract_zip_success(mock_zipfile, copernicus_instance):
    mock_zip = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip

    status, response = copernicus_instance.extract_zip("fake.zip", "output")

    assert status == STATUS_OK
    assert "Extracted fake.zip" in response["message"]
    mock_zip.extractall.assert_called_once_with("output")


### 6. extract_zip failure
def test_extract_zip_failure(copernicus_instance):
    status, response = copernicus_instance.extract_zip("nonexistent.zip", "output")

    assert status == STATUS_BAD_REQUEST
    assert "Error extracting" in response["message"]


### 7. delete_file success
@patch("os.remove")
def test_delete_file_success(mock_remove, copernicus_instance):
    copernicus_instance.delete_file("file.txt")
    mock_remove.assert_called_once_with("file.txt")


### 8. delete_file failure
@patch("os.remove", side_effect=Exception("Permission denied"))
def test_delete_file_failure(mock_remove, copernicus_instance):
    with pytest.raises(Exception) as exc:
        copernicus_instance.delete_file("file.txt")

    assert "Error deleting file.txt" in str(exc.value)


@patch("builtins.open", new_callable=MagicMock)
@patch("requests.Session")
@patch.object(Copernicus, "authenticate", return_value="fake-token")
def test_download_success(mock_auth, mock_session, mock_open, copernicus_instance):
    session_mock = MagicMock()
    mock_session.return_value = session_mock

    redirect_response = MagicMock()
    redirect_response.status_code = 301
    redirect_response.headers = {"Location": "redirected_url"}

    final_response = MagicMock()
    final_response.status_code = 200
    final_response.content = b"fake-zip-content"

    session_mock.get.side_effect = [redirect_response, final_response, final_response]

    copernicus_instance.download(
        product_id=123, identifier="test_file", output_folder="downloads"
    )

    mock_auth.assert_called_once()

    session_mock.headers.update.assert_called_with(
        {"Authorization": "Bearer fake-token"}
    )

    assert session_mock.get.call_count >= 3

    mock_open.assert_called_once_with(os.path.join("downloads", "test_file.zip"), "wb")

    handle = mock_open.return_value.__enter__.return_value
    handle.write.assert_called_once_with(b"fake-zip-content")


@patch.object(Copernicus, "authenticate", return_value="fake-token")
@patch("requests.Session")
def test_download_raises_exception(mock_session, mock_auth, copernicus_instance):
    session_mock = MagicMock()
    mock_session.return_value = session_mock
    session_mock.get.side_effect = Exception("Network error")

    with pytest.raises(Exception) as exc_info:
        copernicus_instance.download(product_id=123, identifier="test_file")

    assert "Error download test_file" in str(exc_info.value)
    assert "Network error" in str(exc_info.value)

    mock_auth.assert_called_once()
