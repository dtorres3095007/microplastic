from typing import Optional
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.query_reader import sql_query_reader
import os
from typing import List, Dict
from datetime import datetime


base_dir = os.path.dirname(os.path.abspath(__file__))


class MediaFilesQueries:
    @sql_query_reader(base_dir, "media_files_post.sql")
    def insert_media_file(
        self,
        type: str,
        title: str,
        url: str,
        thumbnail_url: str,
        description: str,
        conn: DatabaseConnection,
    ) -> Optional[int]:
        """
        This method inserts a media file into the database.

        args:
            type (str): The type of the media file (e.g., 'image', 'video').
            title (str): The title of the media file.
            url (str): The URL of the media file.
            thumbnail_url (str): The URL of the thumbnail image for the media file.
            description (str): A description of the media file.
            conn (DatabaseConnection): The database connection object.
        returns:
            Optional[int]: The ID of the inserted media file, or None if the insertion failed.
        """
        query: str = self.insert_media_file.query
        params = {
            "type": type,
            "title": title,
            "url": url,
            "thumbnail_url": thumbnail_url,
            "description": description,
        }
        resp = conn.execute_update(query, params)
        return resp

    @sql_query_reader(base_dir, "media_files_patch.sql")
    def update_media_file(
        self,
        conn: DatabaseConnection,
        id: int,
        type: str,
        title: str,
        url: str,
        thumbnail_url: Optional[str],
        description: Optional[str],
    ) -> bool:
        """
        This method updates a media file in the database.

        args:
            conn (DatabaseConnection): The database connection object.
            id (int): The ID of the media file to update.
            type (str): The type of the media file (e.g., 'image', 'video').
            title (str): The title of the media file.
            url (str): The URL of the media file.
            thumbnail_url (Optional[str]): The URL of the thumbnail image for the media file.
            description (Optional[str]): A description of the media file.
        returns:
            bool: True if the update was successful, False otherwise.
        """
        query: str = self.update_media_file.query
        params = {
            "id": id,
            "type": type,
            "title": title,
            "url": url,
            "thumbnail_url": thumbnail_url if thumbnail_url else None,
            "description": description,
            "uploaded_at": datetime.now(),
        }
        resp = conn.execute_update(query, params)
        return resp

    @sql_query_reader(base_dir, "media_files_get.sql")
    def get_media_file(
        self,
        conn: DatabaseConnection,
        id: int,
    ) -> Optional[dict]:
        """
        This method retrieves a media file from the database.

        args:
            conn (DatabaseConnection): The database connection object.
            id (int): The ID of the media file to retrieve.
        returns:
            Optional[dict]: A dictionary containing the media file details, or None if not found.
        """
        query: str = self.get_media_file.query
        params = {"id": id}
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "media_files_get_all.sql")
    def get_all_media_files(
        self,
        conn: DatabaseConnection,
        limit: int,
        offset: int,
        search: Optional[str],
    ) -> List[Dict]:
        """
        This method retrieves all media files for a specific collection from the database.

        args:
            conn (DatabaseConnection): The database connection object.
        returns:
            list[dict]: A list of dictionaries containing media file details.
        """
        query: str = self.get_all_media_files.query
        params = {
            "limit": limit,
            "offset": offset,
            "search": search if search else None,
        }
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "media_files_delete.sql")
    def delete_media_file(
        self,
        conn: DatabaseConnection,
        id: int,
    ) -> bool:
        """
        This method deletes a media file from the database.

        args:
            conn (DatabaseConnection): The database connection object.
            id (int): The ID of the media file to delete.
        returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query: str = self.delete_media_file.query
        params = {"id": id}
        resp = conn.execute_update(query, params)
        return resp
