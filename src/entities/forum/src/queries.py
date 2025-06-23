from typing import Optional
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.query_reader import sql_query_reader
import os


base_dir = os.path.dirname(os.path.abspath(__file__))


class ForumQueries:
    @sql_query_reader(base_dir, "forum_post.sql")
    def insert_forum(
        self, content: str, author_name: Optional[str], conn: DatabaseConnection
    ) -> Optional[int]:
        """
        Inserts a new forum post into the database.

        Args:
            content (str): The content of the forum post.
            author_name (Optional[str]): The name of the author of the post.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the inserted forum post, or None if the insertion failed.
        """

        query: str = self.insert_forum.query
        params = {"content": content, "author_name": author_name}
        resp = conn.execute_update(query, params)
        return resp
