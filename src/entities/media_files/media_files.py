from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.src.queries import MediaFilesQueries
from src.shared.db_config import DatabaseConnection
from datetime import datetime


class MediaFiles:
    def __init__(self, conn: DatabaseConnection):
        self.media_queries = MediaFilesQueries()
        self.conn = conn

    def insert_media_file(
        self,
        collection_id: int,
        type: str,
        title: str,
        url: str,
        thumbnail_url: str,
        description: str
    ) -> tuple:
        """
        Inserts a media file into the database.
        
        Args:
            collection_id (int): The ID of the collection to which the media file belongs.
            type (str): The type of the media file (e.g., 'image', 'video').
            title (str): The title of the media file.
            url (str): The URL of the media file.
            thumbnail_url (str): The URL of the thumbnail image for the media file.
            description (str): A description of the media file.
        
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        media_file_id = self.media_queries.insert_media_file(
            collection_id=collection_id,
            type=type,
            title=title,
            url=url,
            thumbnail_url=thumbnail_url,
            description=description,
            conn=self.conn
        )

        if not media_file_id:
            return STATUS_BAD_REQUEST, {"message": "Error inserting media file"}

        return STATUS_OK, {"message": "Media file inserted successfully", "media_file_id": media_file_id}
    
    def update_media_file(
        self,
        id: int,
        type: str,
        title: str,
        url: str,
        thumbnail_url: str = None,
        description: str = None
    ) -> tuple:
        """
        Updates a media file in the database.
        
        Args:
            id (int): The ID of the media file to update.
            type (str): The type of the media file.
            title (str): The title of the media file.
            url (str): The URL of the media file.
            thumbnail_url (str, optional): The URL of the thumbnail image for the media file.
            description (str, optional): A description of the media file.
        
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        updated = self.media_queries.update_media_file(
            conn=self.conn,
            id=id,
            type=type,
            title=title,
            url=url,
            thumbnail_url=thumbnail_url,
            description=description
        )

        if not updated:
            return STATUS_BAD_REQUEST, {"message": "Error updating media file"}

        return STATUS_OK, {"message": "Media file updated successfully"}
    
    def delete_media_file(self, id: int) -> tuple:
        """
        Deletes a media file from the database.
        
        Args:
            id (int): The ID of the media file to delete.
        
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        deleted = self.media_queries.delete_media_file(
            conn=self.conn,
            id=id
        )

        if not deleted:
            return STATUS_BAD_REQUEST, {"message": "Error deleting media file"}

        return STATUS_OK, {"message": "Media file deleted successfully"}
    
    def get_media_file(self, id: int) -> tuple:
        """
        Retrieves a media file from the database.
        
        Args:
            id (int): The ID of the media file to retrieve.
        
        Returns:
            tuple: A tuple containing the status code and the media file details or an error message.
        """
        media_details = self.media_queries.get_media_file(
            conn=self.conn,
            id=id
        )

        if not media_details:
            return STATUS_BAD_REQUEST, {"message": "Media file not found"}

        return STATUS_OK, media_details
    
    def get_all_media_files(self, collection_id: int) -> tuple:
        """
        Retrieves all media files for a specific collection from the database.
        
        Args:
            collection_id (int): The ID of the collection to retrieve media files for.
        
        Returns:
            tuple: A tuple containing the status code and a list of media files or an error message.
        """
        all_media_files = self.media_queries.get_all_media_files(
            conn=self.conn,
            collection_id=collection_id
        )

        if not all_media_files:
            return STATUS_BAD_REQUEST, {"message": "No media files found for this collection"}

        return STATUS_OK, all_media_files
    