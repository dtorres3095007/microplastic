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

    @sql_query_reader(base_dir, "forum_get_all.sql")
    def forum_get_all(
        self, conn: DatabaseConnection, limit: int, offset: int, search: Optional[str]
    ) -> Optional[dict]:
        """
        Retrieves all forum posts from the database.

        Args:
            limit (int): The maximum number of posts to return.
            offset (int): The number of posts to skip before starting to return results.
            search (Optional[str]): An optional search term to filter posts by content.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[dict]: A dictionary containing all forum posts, or None if retrieval failed.
        """

        query: str = self.forum_get_all.query
        params = {"limit": limit, "offset": offset, "search": search}
        resp = conn.execute_query(query, params)
        return resp
