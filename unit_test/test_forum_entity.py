import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.entities.forum.forum import Forum
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_conn():
    return MagicMock()


@pytest.fixture
def forum(mock_conn):
    return Forum(conn=mock_conn)


def test_insert_forum_post_success(forum):
    forum.forum_queries.insert_forum = MagicMock(return_value=1)
    status, response = forum.insert_forum_post(
        content="Hello world", author_name="Luis"
    )
    assert status == STATUS_OK
    assert response["message"] == "Post inserted successfully"
    assert response["status"] == 1


def test_insert_forum_post_failure(forum):
    forum.forum_queries.insert_forum = MagicMock(return_value=None)
    status, response = forum.insert_forum_post(
        content="Hello world", author_name="Luis"
    )
    assert status == STATUS_BAD_REQUEST
    assert response == "Failed to insert forum post."


def test_forum_get_all_success(forum):
    mock_data = [{"id": 1, "content": "Post 1"}, {"id": 2, "content": "Post 2"}]
    forum.forum_queries.forum_get_all = MagicMock(return_value=mock_data)
    status, response = forum.forum_get_all(limit=10, offset=0, search=None)
    assert status == STATUS_OK
    assert isinstance(response, list)
    assert len(response) == 2


def test_forum_get_all_not_found(forum):
    forum.forum_queries.forum_get_all = MagicMock(return_value=None)
    status, response = forum.forum_get_all(limit=10, offset=0, search=None)
    assert status == STATUS_NOT_FOUND
    assert response == {"message": "No forum posts found."}
