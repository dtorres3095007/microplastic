from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.media_files.src.queries import MediaFilesQueries
from src.shared.db_config import DatabaseConnection
from typing import Optional, Tuple
import os
import uuid


class MediaFiles:
    def __init__(self, conn: DatabaseConnection):
        self.media_queries = MediaFilesQueries()
        self.conn = conn
        self.MEDIA_DIR = "media/media_files"

    def _save_file(self, content: bytes, filename: str) -> str:
        extension = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{extension}"
        os.makedirs(self.MEDIA_DIR, exist_ok=True)
        file_path = os.path.join(self.MEDIA_DIR, unique_name)
        with open(file_path, "wb") as f:
            f.write(content)
        return f"/media/media_files/{unique_name}"

    def _delete_file_by_url(self, url_path: Optional[str]):
        if url_path:
            file_path = url_path.replace("/media/media_files/", f"{self.MEDIA_DIR}/")
            if os.path.exists(file_path):
                os.remove(file_path)

    def _require_existing_media(self, id: int) -> Tuple[int, Optional[dict]]:
        status, media = self.get_media_file(id)
        if status != STATUS_OK:
            return STATUS_NOT_FOUND, None
        return STATUS_OK, media[0]

    def insert_media_file(
        self,
        type: str,
        title: str,
        file_content: bytes,
        original_filename: str,
        thumbnail_content: Optional[bytes],
        thumbnail_filename: Optional[str],
        description: Optional[str],
    ) -> Tuple[int, str]:
        """
        Inserts a media file into the database.

        Args:
            type (str): The type of the media file (e.g., 'image', 'video').
            title (str): The title of the media file.
            file_content (bytes): The content of the media file.
            original_filename (str): The original name of the media file.
            thumbnail_content (Optional[bytes]): The content of the thumbnail image.
            thumbnail_filename (Optional[str]): The original name of the thumbnail image.
            description (Optional[str]): A description of the media file.

        Returns:
            tuple: A tuple containing the status code and a message.
        """
        os.makedirs(self.MEDIA_DIR, exist_ok=True)

        url = self._save_file(file_content, original_filename)
        thumbnail_url = None

        if thumbnail_content and thumbnail_filename:
            thumbnail_url = self._save_file(thumbnail_content, thumbnail_filename)

        resp = self.media_queries.insert_media_file(
            type=type,
            title=title,
            url=url,
            thumbnail_url=thumbnail_url,
            description=description,
            conn=self.conn,
        )

        if not resp:
            return STATUS_BAD_REQUEST, {"message": "Error inserting media file"}

        return STATUS_OK, {
            "message": "Media file inserted successfully",
            "status": resp,
        }

    def update_media_file(
        self,
        id: int,
        type: Optional[str],
        title: Optional[str],
        file_content: Optional[bytes],
        original_filename: Optional[str],
        thumbnail_content: Optional[bytes],
        thumbnail_filename: Optional[str],
        description: Optional[str],
    ) -> tuple:
        """
        Updates a media file in the database and optionally replaces physical media or thumbnail.

        Args:
            id (int): ID of the media file to update.
            type (Optional[str]): New type (image, video).
            title (Optional[str]): New title.
            file_content (Optional[bytes]): New file content if being updated.
            original_filename (Optional[str]): Original name of the new file.
            thumbnail_content (Optional[bytes]): New thumbnail content if being updated.
            thumbnail_filename (Optional[str]): Original name of the new thumbnail.
            description (Optional[str]): New description.

        Returns:
            tuple: (status_code, message)
        """
        status_code, media_data = self._require_existing_media(id)
        if not media_data:
            return status_code, {"message": "Previous media file not found"}

        url = None
        thumbnail_url = None

        if file_content and original_filename:
            self._delete_file_by_url(media_data.get("url"))
            url = self._save_file(file_content, original_filename)

        if thumbnail_content and thumbnail_filename:
            self._delete_file_by_url(media_data.get("thumbnail_url"))
            thumbnail_url = self._save_file(thumbnail_content, thumbnail_filename)
        elif thumbnail_content is None and thumbnail_filename is None:
            self._delete_file_by_url(media_data.get("thumbnail_url"))
            thumbnail_url = None

        updated = self.media_queries.update_media_file(
            conn=self.conn,
            id=id,
            type=type,
            title=title,
            url=url,
            thumbnail_url=thumbnail_url,
            description=description,
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
        status, media = self.get_media_file(id=id)
        if status != STATUS_OK:
            return status, media

        self._delete_file_by_url(media[0].get("url"))
        self._delete_file_by_url(media[0].get("thumbnail_url"))

        deleted = self.media_queries.delete_media_file(conn=self.conn, id=id)

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
        media_details = self.media_queries.get_media_file(conn=self.conn, id=id)

        if not media_details:
            return STATUS_NOT_FOUND, {"message": "Media file not found"}

        return STATUS_OK, media_details

    def get_all_media_files(
        self,
        limit: int,
        offset: int,
        search: Optional[str],
    ) -> tuple:
        """
        Retrieves all media files for a specific collection from the database.

        Args:
            limit (int): The maximum number of media files to retrieve (default is 10).
            offset (int): The number of media files to skip before starting to collect the result set.
            search (Optional[str]): A search term to filter media files by title or description.

        Returns:
            tuple: A tuple containing the status code and a list of media files or an error message.
        """
        all_media_files = self.media_queries.get_all_media_files(
            conn=self.conn,
            limit=limit,
            offset=offset,
            search=search,
        )

        if not all_media_files:
            return STATUS_NOT_FOUND, {
                "message": "No media files found for this collection"
            }

        return STATUS_OK, all_media_files
