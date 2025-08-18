import pytest
from unittest.mock import MagicMock, patch
from datetime import date
from src.entities.media_collections.media_collections import MediaCollections
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.media_collections.src.queries import MediaCollectionsQueries


@pytest.fixture
def mock_conn():
    mock = MagicMock()
    mock.execute_update.return_value = 1
    mock.execute_query.return_value = [{"media_id": 1}]
    return mock


@pytest.fixture
def media_collections(mock_conn):
    return MediaCollections(conn=mock_conn)


@pytest.fixture
def sample_media():
    return {
        "media_id": 1,
        "title": "Test Media",
        "summary": "Summary",
        "content": "Content",
        "media_type": "video",
        "media_url": "/media/media_collections/test.mp4",
        "thumbnail_url": "/media/media_collections/thumb.jpg",
        "published_at": date.today(),
        "status": "active",
    }


# --- TEST _save_file ---
@patch("builtins.open", new_callable=MagicMock)
@patch("os.makedirs")
@patch("uuid.uuid4")
def test_save_file_creates_unique_file(
    mock_uuid, mock_makedirs, mock_open, media_collections
):
    mock_uuid.return_value.hex = "123abc"
    file_path = media_collections._save_file(b"content", "video.mp4")

    assert file_path.startswith("/media/media_collections/")
    assert file_path.endswith(".mp4")
    mock_makedirs.assert_called_once_with("media/media_collections", exist_ok=True)
    mock_open.assert_called_once()


# --- TEST insert_media ---
@patch.object(
    MediaCollections,
    "_save_file",
    side_effect=[
        "/media/media_collections/file.mp4",
        "/media/media_collections/thumb.jpg",
    ],
)
def test_insert_media_success(mock_save_file, media_collections):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_update.return_value = 1

    status, response = media_collections.insert_media(
        title="Title",
        summary="Summary",
        content="Content",
        media_type="video",
        file_content=b"video-data",
        original_filename="video.mp4",
        thumbnail_content=b"thumb-data",
        thumbnail_filename="thumb.jpg",
        published_at=date.today(),
        status="active",
    )

    assert status == STATUS_OK
    assert response["message"] == "Media inserted successfully"
    mock_save_file.assert_called()


def test_insert_media_failure(media_collections):
    media_collections._save_file = MagicMock(
        return_value="/media/media_collections/file.mp4"
    )
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_update.return_value = None

    status, response = media_collections.insert_media(
        title="Title",
        summary="Summary",
        content="Content",
        media_type="video",
        file_content=b"video-data",
        original_filename="video.mp4",
        thumbnail_content=None,
        thumbnail_filename=None,
        published_at=date.today(),
        status="active",
    )

    assert status == STATUS_BAD_REQUEST
    assert response["message"] == "Error inserting media"


# --- TEST get_media ---
def test_get_media_found(media_collections, sample_media):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]

    status, response = media_collections.get_media(1)

    assert status == STATUS_OK
    assert response[0]["media_id"] == 1


def test_get_media_not_found(media_collections):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = None

    status, response = media_collections.get_media(1)

    assert status == STATUS_NOT_FOUND
    assert response["message"] == "Media not found"
    media_collections.conn.execute_query.assert_called_once()


# --- TEST get_all_media ---
def test_get_all_media_success(media_collections, sample_media):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]

    status, response = media_collections.get_all_media(limit=10, offset=0, search=None)

    assert status == STATUS_OK
    assert isinstance(response, list)


def test_get_all_media_empty(media_collections):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = None

    status, response = media_collections.get_all_media(limit=10, offset=0, search=None)

    assert status == STATUS_BAD_REQUEST
    assert response["message"] == "No media found"


@patch.object(MediaCollections, "_delete_file_by_url")
def test_delete_media_success(mock_delete_file, media_collections, sample_media):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]
    media_collections.conn.execute_update.return_value = 1

    status, response = media_collections.delete_media(1)

    assert status == STATUS_OK
    assert response["message"] == "Media deleted successfully"
    mock_delete_file.assert_called()


def test_delete_media_not_found(media_collections):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = None

    status, response = media_collections.delete_media(1)

    assert status == STATUS_NOT_FOUND


# --- TEST update_media ---
@patch.object(
    MediaCollections, "_save_file", side_effect=["/media/media_collections/newfile.mp4"]
)
@patch.object(MediaCollections, "_delete_file_by_url")
def test_update_media_success(
    mock_delete_file, mock_save_file, media_collections, sample_media
):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]
    media_collections.conn.execute_update.return_value = 1

    status, response = media_collections.update_media(
        media_id=1,
        title="New Title",
        summary="New Summary",
        content="New Content",
        media_type="video",
        file_content=b"new video",
        original_filename="new_video.mp4",
        thumbnail_content=None,
        thumbnail_filename=None,
        published_at=date.today(),
        status="active",
    )

    assert status == STATUS_OK
    assert response["message"] == "Media updated successfully"
    mock_save_file.assert_called()


def test_update_media_not_found(media_collections):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = None
    media_collections.conn.execute_update.return_value = 1

    status, response = media_collections.update_media(
        media_id=1,
        title="New Title",
        summary="New Summary",
        content="New Content",
        media_type="video",
        file_content=None,
        original_filename=None,
        thumbnail_content=None,
        thumbnail_filename=None,
        published_at=date.today(),
        status="active",
    )

    assert status == STATUS_NOT_FOUND


@patch("os.remove")
@patch("os.path.exists", return_value=True)
def test_delete_file_by_url_removes_file(mock_exists, mock_remove, media_collections):
    url = "/media/media_collections/test.mp4"
    media_collections._delete_file_by_url(url)
    mock_exists.assert_called_once()
    mock_remove.assert_called_once()


def test_delete_file_by_url_no_url(media_collections):
    media_collections._delete_file_by_url(None)
    media_collections._delete_file_by_url("")


@patch("os.path.exists", return_value=False)
def test_delete_file_by_url_file_not_exists(mock_exists, media_collections):
    url = "/media/media_collections/nonexistent.mp4"
    media_collections._delete_file_by_url(url)
    mock_exists.assert_called_once()


@patch.object(MediaCollections, "_delete_file_by_url")
def test_delete_media_failure(mock_delete_file, media_collections, sample_media):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]
    media_collections.conn.execute_update.return_value = 0

    status, response = media_collections.delete_media(1)

    assert status == STATUS_BAD_REQUEST
    assert response["message"] == "Error deleting media"
    mock_delete_file.assert_not_called()


@patch.object(
    MediaCollections,
    "_save_file",
    side_effect=[
        "/media/media_collections/newfile.mp4",
        "/media/media_collections/newthumb.jpg",
    ],
)
@patch.object(MediaCollections, "_delete_file_by_url")
def test_update_media_with_thumbnail(
    mock_delete_file, mock_save_file, media_collections, sample_media
):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]
    media_collections.conn.execute_update.return_value = 1

    status, response = media_collections.update_media(
        media_id=1,
        title="New Title",
        summary="New Summary",
        content="New Content",
        media_type="video",
        file_content=b"new video",
        original_filename="new_video.mp4",
        thumbnail_content=b"new thumb",
        thumbnail_filename="new_thumb.jpg",
        published_at=date.today(),
        status="active",
    )

    assert status == STATUS_OK
    assert response["message"] == "Media updated successfully"
    assert mock_save_file.call_count == 2


def test_update_media_failure(media_collections, sample_media):
    media_collections.media_queries = MediaCollectionsQueries()
    media_collections.conn.execute_query.return_value = [sample_media]
    media_collections.conn.execute_update.return_value = 0

    status, response = media_collections.update_media(
        media_id=1,
        title="Title",
        summary="Summary",
        content="Content",
        media_type="video",
        file_content=None,
        original_filename=None,
        thumbnail_content=b"new thumb",
        thumbnail_filename=None,
        published_at=date.today(),
        status="active",
    )

    assert status == STATUS_BAD_REQUEST
    assert response["message"] == "Error updating media"
