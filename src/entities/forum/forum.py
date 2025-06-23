from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.forum.src.queries import ForumQueries
from src.shared.db_config import DatabaseConnection
from typing import Optional, Tuple


class Forum:
    def __init__(self, conn: DatabaseConnection):
        self.forum_queries = ForumQueries()
        self.conn = conn

    def insert_forum_post(
        self, content: str, author_name: Optional[str]
    ) -> Tuple[int, str]:
        """
        Inserts a new forum post into the database.

        Args:
            content (str): The content of the forum post.
            author_name (Optional[str]): The name of the author of the post.

        Returns:
            tuple: A tuple containing the status code and a message.
        """
        resp = self.forum_queries.insert_forum(content, author_name, self.conn)
        if resp is None:
            return STATUS_BAD_REQUEST, "Failed to insert forum post."

        return STATUS_OK, {
            "message": "Post inserted successfully",
            "status": resp,
        }

    def forum_get_all(
        self, limit: int, offset: int, search: Optional[str]
    ) -> Tuple[int, dict]:
        """
        Retrieves all forum posts from the database.

        Args:
            limit (int): The maximum number of posts to return.
            offset (int): The number of posts to skip before starting to return results.
            search (Optional[str]): An optional search term to filter posts by content.
            conn (DatabaseConnection): The database connection object.

        Returns:
            tuple: A tuple containing the status code and a list of forum posts or None if retrieval failed.
        """
        resp = self.forum_queries.forum_get_all(
            conn=self.conn, limit=limit, offset=offset, search=search
        )
        if resp is None:
            return STATUS_NOT_FOUND, {"message": "No forum posts found."}

        return STATUS_OK, resp
