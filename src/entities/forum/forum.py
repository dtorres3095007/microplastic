from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
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
        if not content:
            return STATUS_BAD_REQUEST, "Content cannot be empty."

        resp = self.forum_queries.insert_forum(content, author_name, self.conn)
        if resp is None:
            return STATUS_BAD_REQUEST, "Failed to insert forum post."

        return STATUS_OK, {
            "message": "Post inserted successfully",
            "status": resp,
        }
