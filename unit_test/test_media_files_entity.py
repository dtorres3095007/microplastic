import pytest
import os
import uuid
from unittest.mock import patch, MagicMock
from src.entities.media_files.media_files import MediaFiles
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND


@pytest.fixture
def mock_conn():
    return MagicMock()


@pytest.fixture
def media_files(mock_conn):
    return MediaFiles(conn=mock_conn)


# --------------------------
# Tests for _save_file
# --------------------------
def test_save_file_creates_file(media_files, tmp_path):
    media_files.MEDIA_DIR = tmp_path
    content = b"test content"
    filename = "file.txt"

    path = media_files._save_file(content, filename)

    assert path.startswith("/media/media_files/")
    full_path = os.path.join(tmp_path, os.path.basename(path))
    assert os.path.exists(full_path)
    with open(full_path, "rb") as f:
        assert f.read() == content


# --------------------------
# Tests for _delete_file_by_url
# --------------------------
def test_delete_file_by_url_removes_existing_file(media_files, tmp_path):
    media_files.MEDIA_DIR = tmp_path
    file_path = tmp_path / "test.txt"
    file_path.write_text("to delete")

    url_path = f"/media/media_files/{file_path.name}"
    media_files._delete_file_by_url(url_path)

    assert not file_path.exists()


def test_delete_file_by_url_does_nothing_if_not_exists(media_files):
    # No error should occur
    media_files._delete_file_by_url("/media/media_files/nonexistent.txt")


# --------------------------
# Tests for insert_media_file
# --------------------------
@patch("src.entities.media_files.media_files.MediaFilesQueries.insert_media_file")
def test_insert_media_file_success(mock_insert, media_files, tmp_path):
    mock_insert.return_value = 123  # Simulate ID returned by the DB
    media_files.MEDIA_DIR = tmp_path

    status, resp = media_files.insert_media_file(
        type="image",
        title="Test Image",
        file_content=b"content",
        original_filename="file.jpg",
        thumbnail_content=None,
        thumbnail_filename=None,
        description="desc",
    )

    assert status == STATUS_OK
    assert "Media file inserted successfully" in resp["message"]
    assert resp["status"] == 123


@patch("src.entities.media_files.media_files.MediaFilesQueries.insert_media_file")
def test_insert_media_file_failure(mock_insert, media_files, tmp_path):
    mock_insert.return_value = None
    media_files.MEDIA_DIR = tmp_path

    status, resp = media_files.insert_media_file(
        type="image",
        title="Test Image",
        file_content=b"content",
        original_filename="file.jpg",
        thumbnail_content=None,
        thumbnail_filename=None,
        description="desc",
    )

    assert status == STATUS_BAD_REQUEST
    assert "Error inserting media file" in resp["message"]


# --------------------------
# Tests for update_media_file
# --------------------------
@patch.object(MediaFiles, "get_media_file")
@patch("src.entities.media_files.media_files.MediaFilesQueries.update_media_file")
def test_update_media_file_success(mock_update, mock_get_media, media_files, tmp_path):
    mock_get_media.return_value = (STATUS_OK, [{"url": None, "thumbnail_url": None}])
    mock_update.return_value = True
    media_files.MEDIA_DIR = tmp_path

    status, resp = media_files.update_media_file(
        id=1,
        type="image",
        title="Updated Title",
        file_content=None,
        original_filename=None,
        thumbnail_content=None,
        thumbnail_filename=None,
        description="Updated desc",
    )

    assert status == STATUS_OK
    assert "Media file updated successfully" in resp["message"]


@patch.object(MediaFiles, "get_media_file")
def test_update_media_file_not_found(mock_get_media, media_files):
    mock_get_media.return_value = (STATUS_NOT_FOUND, None)

    status, resp = media_files.update_media_file(
        id=999,
        type=None,
        title=None,
        file_content=None,
        original_filename=None,
        thumbnail_content=None,
        thumbnail_filename=None,
        description=None,
    )

    assert status == STATUS_NOT_FOUND
    assert "Previous media file not found" in resp["message"]


# --------------------------
# Tests for delete_media_file
# --------------------------
@patch.object(MediaFiles, "get_media_file")
@patch("src.entities.media_files.media_files.MediaFilesQueries.delete_media_file")
def test_delete_media_file_success(mock_delete, mock_get_media, media_files):
    mock_get_media.return_value = (STATUS_OK, [{"url": None, "thumbnail_url": None}])
    mock_delete.return_value = True

    status, resp = media_files.delete_media_file(1)

    assert status == STATUS_OK
    assert "Media file deleted successfully" in resp["message"]


@patch.object(MediaFiles, "get_media_file")
def test_delete_media_file_not_found(mock_get_media, media_files):
    mock_get_media.return_value = (
        STATUS_NOT_FOUND,
        {"message": "Media file not found"},
    )

    status, resp = media_files.delete_media_file(999)

    assert status == STATUS_NOT_FOUND
    assert "Media file not found" in resp["message"]


# --------------------------
# Tests for get_media_file and get_all_media_files
# --------------------------
@patch("src.entities.media_files.media_files.MediaFilesQueries.get_media_file")
def test_get_media_file_found(mock_get, media_files):
    mock_get.return_value = [{"id": 1, "title": "Sample"}]

    status, data = media_files.get_media_file(1)

    assert status == STATUS_OK
    assert data[0]["title"] == "Sample"


@patch("src.entities.media_files.media_files.MediaFilesQueries.get_media_file")
def test_get_media_file_not_found(mock_get, media_files):
    mock_get.return_value = None

    status, data = media_files.get_media_file(999)

    assert status == STATUS_NOT_FOUND
    assert "Media file not found" in data["message"]


@patch("src.entities.media_files.media_files.MediaFilesQueries.get_all_media_files")
def test_get_all_media_files_found(mock_get, media_files):
    mock_get.return_value = [{"id": 1, "title": "File1"}]

    status, data = media_files.get_all_media_files(limit=10, offset=0, search=None)

    assert status == STATUS_OK
    assert len(data) == 1


@patch("src.entities.media_files.media_files.MediaFilesQueries.get_all_media_files")
def test_get_all_media_files_not_found(mock_get, media_files):
    mock_get.return_value = None

    status, data = media_files.get_all_media_files(limit=10, offset=0, search=None)

    assert status == STATUS_NOT_FOUND
    assert "No media files found" in data["message"]
