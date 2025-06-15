from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.src.queries import MediaCollectionsQueries
from src.shared.db_config import DatabaseConnection
from datetime import date


class MediaCollections:
    def __init__(self, conn: DatabaseConnection):
        self.media_queries = MediaCollectionsQueries()
        self.conn = conn

    def insert_media(self, title: str, description: str = None, date: date = None) -> tuple:
        """
        This method will insert a media collection into the database.
        Args:
            title (str): The title of the media collection.
            description (str): The description of the media collection.
            date (str): The date of the media collection.
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        media_collections = self.media_queries.insert_media(
            title=title,
            description=description,
            date=date,
            conn=self.conn,
        )

        if not media_collections:
            return STATUS_BAD_REQUEST, {"message": "Error inserting media"}

        return STATUS_OK, {"message": "Media inserted successfully"}
    
    def get_media(self, media_id: int) -> tuple:
        """
        This method retrieves media details from the database.
        Args:
            media_id (int): The ID of the media to retrieve.
        Returns:
            tuple: A tuple containing the status code and the media details or an error message.
        """
        media_details = self.media_queries.get_media(
            media_id=media_id,
            conn=self.conn,
        )

        if not media_details:
            return STATUS_BAD_REQUEST, {"message": "Media not found"}

        return STATUS_OK, media_details
    
    def get_all_media(self) -> tuple:
        """
        This method retrieves all media collections from the database.
        Returns:
            tuple: A tuple containing the status code and a list of all media collections or an error message.
        """
        all_media = self.media_queries.get_all_media(
            conn=self.conn,
        )

        if not all_media:
            return STATUS_BAD_REQUEST, {"message": "No media found"}

        return STATUS_OK, all_media
    
    def delete_media(self, media_id: int) -> tuple:
        """
        This method deletes a media collection from the database.
        Args:
            media_id (int): The ID of the media collection to delete.
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        deleted_media = self.media_queries.delete_media(
            media_id=media_id,
            conn=self.conn,
        )

        if not deleted_media:
            return STATUS_BAD_REQUEST, {"message": "Error deleting media"}

        return STATUS_OK, {"message": "Media deleted successfully"}
    
    def update_media(self, media_id: int, title: str, description: str = None, date: date = None) -> tuple:
        """
        This method updates a media collection in the database.
        Args:
            media_id (int): The ID of the media collection to update.
            title (str): The new title of the media collection.
            description (str): The new description of the media collection.
            date (str): The new date of the media collection.
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        updated_media = self.media_queries.update_media(
            media_id=media_id,
            title=title,
            description=description,
            date=date,
            conn=self.conn,
        )

        if not updated_media:
            return STATUS_BAD_REQUEST, {"message": "Error updating media"}

        return STATUS_OK, {"message": "Media updated successfully"}
