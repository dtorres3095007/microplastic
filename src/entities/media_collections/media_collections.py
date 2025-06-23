from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.media_collections.src.queries import MediaCollectionsQueries
from src.shared.db_config import DatabaseConnection
from datetime import date
from typing import Optional, Tuple
import os
import uuid


class MediaCollections:
    def __init__(self, conn: DatabaseConnection):
        self.media_queries = MediaCollectionsQueries()
        self.conn = conn
        self.created_by = 1
        self.updated_by = 1
        self.MEDIA_DIR = "media/media_collections"

    def _save_file(self, content: bytes, filename: str) -> str:
        os.makedirs(self.MEDIA_DIR, exist_ok=True)
        extension = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{extension}"
        file_path = os.path.join(self.MEDIA_DIR, unique_name)
        with open(file_path, "wb") as f:
            f.write(content)
        return f"/media/media_collections/{unique_name}"

    def _delete_file_by_url(self, url: str):
        if url:
            file_path = url.replace("/media/media_collections/", self.MEDIA_DIR + "/")
            if os.path.exists(file_path):
                os.remove(file_path)

    def insert_media(
        self,
        title: str,
        summary: str,
        content: str,
        media_type: str,
        file_content: bytes,
        original_filename: str,
        thumbnail_content: Optional[bytes],
        thumbnail_filename: Optional[str],
        published_at: date,
        status: str,
    ) -> Tuple[int, dict]:
        """
        This method inserts a new media record into the database.

        Args:
            title (str): The title of the media.
            summary (str): A brief summary of the media.
            content (str): The content of the media.
            media_type (str): The type of media (e.g., video, image).
            file_content (bytes): The content of the media file.
            original_filename (str): The original name of the media file.
            thumbnail_content (Optional[bytes]): The content of the thumbnail image.
            thumbnail_filename (Optional[str]): The original name of the thumbnail image.
            published_at (Optional[date]): The date the media was published.
            status (str): The status of the media (e.g., active, inactive).

        Returns:
            tuple: A tuple containing the status code and a message or media ID.
        """
        media_url = self._save_file(file_content, original_filename)
        thumbnail_url = (
            self._save_file(thumbnail_content, thumbnail_filename)
            if thumbnail_content and thumbnail_filename
            else None
        )

        inserted = self.media_queries.insert_media(
            title=title,
            summary=summary,
            content=content,
            media_type=media_type,
            media_url=media_url,
            thumbnail_url=thumbnail_url,
            published_at=published_at,
            status=status,
            created_by=self.created_by,
            conn=self.conn,
        )

        if not inserted:
            return STATUS_BAD_REQUEST, {"message": "Error inserting media"}

        return STATUS_OK, {"message": "Media inserted successfully"}

    def get_media(self, media_id: int) -> Tuple[int, dict]:
        """
        This method retrieves media details by its ID.

        Args:
            media_id (int): The ID of the media to retrieve.

        Returns:
            tuple: A tuple containing the status code and media details or an error message.
        """
        media = self.media_queries.get_media(media_id=media_id, conn=self.conn)
        if not media:
            return STATUS_NOT_FOUND, {"message": "Media not found"}
        return STATUS_OK, media

    def get_all_media(
        self, limit: int, offset: int, search: Optional[str]
    ) -> Tuple[int, dict]:
        """
        This method retrieves all media records with optional pagination and search.

        Args:
            limit (int): The maximum number of media records to retrieve.
            offset (int): The number of records to skip for pagination.
            search (Optional[str]): A search term to filter media records.

        Returns:
            tuple: A tuple containing the status code and a list of media records or an error message
        """
        media_list = self.media_queries.get_all_media(
            conn=self.conn, limit=limit, offset=offset, search=search
        )
        if not media_list:
            return STATUS_BAD_REQUEST, {"message": "No media found"}
        return STATUS_OK, media_list

    def delete_media(self, media_id: int) -> Tuple[int, dict]:
        """
        This method deletes a media record by its ID.

        Args:
            media_id (int): The ID of the media to delete.

        Returns:
            tuple: A tuple containing the status code and a message indicating success or failure.
        """
        status, media = self.get_media(media_id)
        if status != STATUS_OK:
            return status, media

        self._delete_file_by_url(media[0].get("media_url"))
        self._delete_file_by_url(media[0].get("thumbnail_url"))

        deleted = self.media_queries.delete_media(media_id=media_id, conn=self.conn)
        if not deleted:
            return STATUS_BAD_REQUEST, {"message": "Error deleting media"}

        return STATUS_OK, {"message": "Media deleted successfully"}

    def update_media(
        self,
        media_id: int,
        title: str,
        summary: str,
        content: str,
        media_type: str,
        file_content: Optional[bytes],
        original_filename: Optional[str],
        thumbnail_content: Optional[bytes],
        thumbnail_filename: Optional[str],
        published_at: Optional[date],
        status: str,
    ) -> Tuple[int, dict]:
        """
        This method updates an existing media record.

        Args:
            media_id (int): The ID of the media to update.
            title (str): The new title of the media.
            summary (str): The new summary of the media.
            content (str): The new content of the media.
            media_type (str): The new type of media.
            file_content (Optional[bytes]): The new content of the media file.
            original_filename (Optional[str]): The original name of the media file.
            thumbnail_content (Optional[bytes]): The new content of the thumbnail image.
            thumbnail_filename (Optional[str]): The original name of the thumbnail image.
            published_at (Optional[date]): The new date the media was published.
            status (str): The new status of the media.

        Returns:
            tuple: A tuple containing the status code and a message indicating success or failure.
        """
        status_check, media = self.get_media(media_id)
        if status_check != STATUS_OK:
            return status_check, media

        media_url = None
        thumbnail_url = None

        if file_content and original_filename:
            self._delete_file_by_url(media[0].get("media_url"))
            media_url = self._save_file(file_content, original_filename)

        if thumbnail_content and thumbnail_filename:
            self._delete_file_by_url(media[0].get("thumbnail_url"))
            thumbnail_url = self._save_file(thumbnail_content, thumbnail_filename)
        elif not thumbnail_content and not thumbnail_filename:
            self._delete_file_by_url(media[0].get("thumbnail_url"))

        updated = self.media_queries.update_media(
            media_id=media_id,
            title=title,
            summary=summary,
            content=content,
            media_type=media_type,
            media_url=media_url,
            thumbnail_url=thumbnail_url,
            published_at=published_at,
            status=status,
            updated_by=self.updated_by,
            conn=self.conn,
        )

        if not updated:
            return STATUS_BAD_REQUEST, {"message": "Error updating media"}

        return STATUS_OK, {"message": "Media updated successfully"}
