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
        description: str,
        date: date,
        conn: DatabaseConnection,
    ) -> Optional[int]:
        """
        This method will delete an activity into the database.

        args:
            title (str): The title of the media.
            description (str): The description of the media.
            date (datetime): The date of the media.
            conn (DatabaseConnection): The database connection object.
        Returns:
            Optional[int]: The ID of the inserted media if successful, None otherwise.
        """
        query: str = self.insert_media.query
        params = {
            "title": title,
            "description": description,
            "date": date,
            "created_by": 1,
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
        search: Optional[str] = None,
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
        params = {
            "media_id": media_id
        }
        resp = conn.execute_update(query, params)
        return resp
    
    @sql_query_reader(base_dir, "update_media.sql")
    def update_media(
        self,
        media_id: int,
        title: str,
        description: str,
        date: date,
        conn: DatabaseConnection,
        updated_by: int = 1,
    ) -> Optional[int]:
        """
        This method updates media details in the database.

        args:
            media_id (int): The ID of the media to update.
            title (str): The new title of the media.
            description (str): The new description of the media.
            date (datetime): The new date of the media.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the updated media if successful, None otherwise.
        """
        query: str = self.update_media.query
        params = {
            "media_id": media_id,
            "title": title,
            "description": description,
            "date": date,
            "updated_at": datetime.now(),
            "updated_by": updated_by,
        }
        resp = conn.execute_update(query, params)
        return resp
    