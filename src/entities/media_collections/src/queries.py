from typing import Optional
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.query_reader import sql_query_reader
import os
from datetime import date
from datetime import datetime


base_dir = os.path.dirname(os.path.abspath(__file__))


class MediaCollectionsQueries:
    @sql_query_reader(base_dir, "insert_media.sql")
    def insert_media(
        self,
        title: str,
        summary: str,
        content: str,
        media_type: str,
        media_url: str,
        thumbnail_url: Optional[str],
        published_at: Optional[date],
        status: str,
        conn: DatabaseConnection,
    ) -> Optional[int]:
        """
        This method inserts a new media record into the database.

        args:
            title (str): The title of the media.
            summary (str): A brief summary of the media.
            content (str): The content of the media.
            media_type (str): The type of media (e.g., video, image).
            media_url (str): The URL of the media.
            thumbnail_url (Optional[str]): The URL of the thumbnail image.
            published_at (Optional[date]): The date the media was published.
            status (str): The status of the media (e.g., active, inactive).
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the newly inserted media if successful, None otherwise.
        """
        query: str = self.insert_media.query
        params = {
            "title": title,
            "summary": summary,
            "content": content,
            "media_type": media_type,
            "media_url": media_url,
            "thumbnail_url": thumbnail_url,
            "published_at": published_at,
            "status": status,
        }
        resp = conn.execute_update(query, params)
        return resp

    @sql_query_reader(base_dir, "get_media.sql")
    def get_media(
        self,
        media_id: int,
        conn: DatabaseConnection,
    ) -> Optional[dict]:
        """
        This method retrieves media details from the database.

        args:
            media_id (int): The ID of the media to retrieve.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[dict]: The media details if found, None otherwise.
        """
        query: str = self.get_media.query
        params = {
            "media_id": media_id,
        }
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "get_all_media.sql")
    def get_all_media(
        self,
        conn: DatabaseConnection,
        limit: int,
        offset: int,
        search: Optional[str],
    ) -> Optional[list]:
        """
        This method retrieves all media from the database.

        args:
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[list]: A list of all media if found, None otherwise.
        """
        query: str = self.get_all_media.query
        params = {
            "limit": limit,
            "offset": offset,
            "search": search if search else None,
        }
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "delete_media.sql")
    def delete_media(
        self,
        media_id: int,
        conn: DatabaseConnection,
    ) -> Optional[int]:
        """
        This method deletes media from the database.

        args:
            media_id (int): The ID of the media to delete.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the deleted media if successful, None otherwise.
        """
        query: str = self.delete_media.query
        params = {"media_id": media_id}
        resp = conn.execute_update(query, params)
        return resp

    @sql_query_reader(base_dir, "update_media.sql")
    def update_media(
        self,
        media_id: int,
        title: str,
        summary: str,
        content: str,
        media_type: str,
        media_url: str,
        thumbnail_url: Optional[str],
        published_at: Optional[date],
        status: str,
        conn: DatabaseConnection,
    ) -> Optional[int]:
        """
        This method updates media details in the database.

        args:
            media_id (int): The ID of the media to update.
            title (str): The new title of the media.
            summary (str): The new summary of the media.
            content (str): The new content of the media.
            media_type (str): The new type of media (e.g., video, image).
            media_url (str): The new URL of the media.
            thumbnail_url (Optional[str]): The new URL of the thumbnail image.
            published_at (Optional[date]): The new date the media was published.
            status (str): The new status of the media (e.g., active, inactive).
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the updated media if successful, None otherwise.
        """
        query: str = self.update_media.query
        params = {
            "media_id": media_id,
            "title": title,
            "summary": summary,
            "content": content,
            "media_type": media_type,
            "media_url": media_url,
            "thumbnail_url": thumbnail_url,
            "published_at": published_at,
            "status": status,
            "updated_at": datetime.now(),
        }
        resp = conn.execute_update(query, params)
        return resp
