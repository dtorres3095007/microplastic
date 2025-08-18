import pytest
import os
import uuid
from unittest.mock import patch, MagicMock
from src.entities.media_files.media_files import MediaFiles
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.media_files.src.queries import MediaFilesQueries


@pytest.fixture
def mock_conn():
    mock = MagicMock()
    mock.execute_update.return_value = 1
    mock.execute_query.return_value = [{"id": 1}]
    return mock


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
    media_files._delete_file_by_url("/media/media_files/nonexistent.txt")


# --------------------------
# Tests for insert_media_file
# --------------------------
def test_insert_media_file_success(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_update.return_value = 1

    status, resp = media_files.insert_media_file(
        type="image",
        title="Test Image",
        file_content=b"content",
        original_filename="file.jpg",
        thumbnail_content=b"thumb-content",
        thumbnail_filename="thumb.jpg",
        description="desc",
    )

    assert status == STATUS_OK
    assert "Media file inserted successfully" in resp["message"]


def test_insert_media_file_failure(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_update.return_value = None

    status, resp = media_files.insert_media_file(
        type="image",
        title="Test Image",
        file_content=b"content",
        original_filename="file.jpg",
        thumbnail_content=b"thumb-content",
        thumbnail_filename="thumb.jpg",
        description="desc",
    )

    assert status == STATUS_BAD_REQUEST
    assert "Error inserting media file" in resp["message"]


# --------------------------
# Tests for update_media_file
# --------------------------
def test_update_media_file_success(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]
    media_files.conn.execute_update.return_value = 1

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


def test_update_media_file_not_found(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = None

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
def test_delete_media_file_success(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]
    media_files.conn.execute_update.return_value = 1

    status, resp = media_files.delete_media_file(1)

    assert status == STATUS_OK
    assert "Media file deleted successfully" in resp["message"]


def test_delete_media_file_not_found(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = None

    status, resp = media_files.delete_media_file(999)

    assert status == STATUS_NOT_FOUND
    assert "Media file not found" in resp["message"]


# --------------------------
# Tests for get_media_file and get_all_media_files
# --------------------------
def test_get_media_file_found(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]

    status, data = media_files.get_media_file(1)

    assert status == STATUS_OK
    assert data[0]["title"] == "Test Image"


def test_get_media_file_not_found(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = None

    status, data = media_files.get_media_file(999)

    assert status == STATUS_NOT_FOUND
    assert "Media file not found" in data["message"]


def test_get_all_media_files_found(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]

    status, data = media_files.get_all_media_files(limit=10, offset=0, search=None)

    assert status == STATUS_OK
    assert len(data) == 1


def test_get_all_media_files_not_found(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = None

    status, data = media_files.get_all_media_files(limit=10, offset=0, search=None)

    assert status == STATUS_NOT_FOUND
    assert "No media files found" in data["message"]


def test_update_media_file_with_file_and_thumbnail(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]
    media_files.conn.execute_update.return_value = 1

    status, resp = media_files.update_media_file(
        id=1,
        type="image",
        title="Updated Title",
        file_content=b"new content",
        original_filename="file.jpg",
        thumbnail_content=b"thumb content",
        thumbnail_filename="thumb.jpg",
        description="Updated desc",
    )

    assert status == STATUS_OK
    assert "Media file updated successfully" in resp["message"]


def test_update_media_file_failure(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]
    media_files.conn.execute_update.return_value = None

    status, resp = media_files.update_media_file(
        id=1,
        type="image",
        title="Fail Update",
        file_content=None,
        original_filename=None,
        thumbnail_content=None,
        thumbnail_filename=None,
        description="desc",
    )

    assert status == STATUS_BAD_REQUEST
    assert "Error updating media file" in resp["message"]


def test_delete_media_file_failure(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": b"content",
            "original_filename": "file.jpg",
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": "thumb.jpg",
            "description": "desc",
        }
    ]
    media_files.conn.execute_update.return_value = None

    status, resp = media_files.delete_media_file(1)

    assert status == STATUS_BAD_REQUEST
    assert "Error deleting media file" in resp["message"]


def test_update_media_thumbnail_only_content(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_query.return_value = [
        {
            "id": 1,
            "type": "image",
            "title": "Test Image",
            "file_content": None,
            "original_filename": None,
            "thumbnail_content": b"thumb-content",
            "thumbnail_filename": None,
            "description": "desc",
        }
    ]
    media_files.conn.execute_update.return_value = 1

    status, resp = media_files.update_media_file(
        id=1,
        type="image",
        title="Fail Update",
        file_content=None,
        original_filename=None,
        thumbnail_content=b"thumb content",
        thumbnail_filename=None,
        description="desc",
    )

    assert status == STATUS_OK
    assert "Media file updated successfully" in resp["message"]


def test_insert_media_file_thumbnail_only_content(media_files):
    media_files.media_queries = MediaFilesQueries()
    media_files.conn.execute_update.return_value = 1

    status, resp = media_files.insert_media_file(
        type="image",
        title="Test Image",
        file_content=b"content",
        original_filename="file.jpg",
        thumbnail_content=b"thumb content",
        thumbnail_filename=None,
        description="desc",
    )

    assert status == STATUS_OK
    assert "Media file inserted successfully" in resp["message"]
