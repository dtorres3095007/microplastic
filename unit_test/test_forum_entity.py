import sys
import os
import pytest
from unittest.mock import MagicMock
from src.entities.forum.forum import Forum
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.forum.src.queries import ForumQueries

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def mock_conn():
    mock = MagicMock()
    mock.execute_update.return_value = 1
    mock.execute_query.return_value = [{"id": 1, "content": "Hello"}]
    return mock


@pytest.fixture
def forum(mock_conn):
    return Forum(conn=mock_conn)


def test_insert_forum_post_success(forum):
    forum.forum_queries = ForumQueries()
    forum.conn.execute_update.return_value = 1

    status, response = forum.insert_forum_post(
        content="Hello world", author_name="Luis"
    )

    assert status == STATUS_OK
    assert response["message"] == "Post inserted successfully"
    assert response["status"] == 1
    forum.conn.execute_update.assert_called_once()


def test_insert_forum_post_failure(forum):
    forum.forum_queries = ForumQueries()
    forum.conn.execute_update.return_value = None

    status, response = forum.insert_forum_post(
        content="Hello world", author_name="Luis"
    )

    assert status == STATUS_BAD_REQUEST
    assert response == "Failed to insert forum post."
    forum.conn.execute_update.assert_called_once()


def test_forum_get_all_success(forum):
    forum.forum_queries = ForumQueries()
    forum.conn.execute_query.return_value = [
        {"id": 1, "content": "Post 1"},
        {"id": 2, "content": "Post 2"},
    ]

    status, response = forum.forum_get_all(limit=10, offset=0, search=None)

    assert status == STATUS_OK
    assert isinstance(response, list)
    assert len(response) == 2
    forum.conn.execute_query.assert_called_once()


def test_forum_get_all_not_found(forum):
    forum.forum_queries = ForumQueries()
    forum.conn.execute_query.return_value = None

    status, response = forum.forum_get_all(limit=10, offset=0, search=None)

    assert status == STATUS_NOT_FOUND
    assert response == {"message": "No forum posts found."}
    forum.conn.execute_query.assert_called_once()
