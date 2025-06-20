from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.src.queries import MediaFilesQueries
from src.shared.db_config import DatabaseConnection
from datetime import datetime
from typing import Optional, Tuple
import os
import uuid


class MediaFiles:
    def __init__(self, conn: DatabaseConnection):
        self.media_queries = MediaFilesQueries()
        self.conn = conn
        self.updated_by = 1

    def insert_media_file(
        self,
        collection_id: str,
        type: str,
        title: str,
        file_content: bytes,
        original_filename: str,
        thumbnail_url: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Tuple[int, str]:
        """
        Inserts a media file into the database.
        
        Args:
            collection_id (int): The ID of the collection to which the media file belongs.
            type (str): The type of the media file (e.g., 'image', 'video').
            title (str): The title of the media file.
            file_content (bytes): The content of the media file.
            original_filename (str): The original name of the media file.
            thumbnail_url (Optional[str]): The URL of the thumbnail image for the media file.
            description (Optional[str]): A description of the media file.
        
        Returns:
            tuple: A tuple containing the status code and a message.
        """
        MEDIA_DIR = "media/media_files"
        os.makedirs(MEDIA_DIR, exist_ok=True)

        # Create a unique filename for the media file
        extension = os.path.splitext(original_filename)[1]
        unique_name = f"{uuid.uuid4().hex}{extension}"
        file_path = os.path.join(MEDIA_DIR, unique_name)

        # Save the file content to the filesystem
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Generate the URL for the media file
        url = f"/media/media_files/{unique_name}"

        resp = self.media_queries.insert_media_file(
            collection_id=int(collection_id),
            type=type,
            title=title,
            url=url,
            thumbnail_url=thumbnail_url,
            description=description,
            conn=self.conn,
        )

        if not resp:
            return STATUS_BAD_REQUEST, {"message": "Error inserting media file"}

        return STATUS_OK, {"message": "Media file inserted successfully", "media_file_id": resp}
    
    def update_media_file(
        self,
        id: int,
        type: Optional[str],
        title: Optional[str],
        file_content: Optional[bytes] = None,
        original_filename: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        description: Optional[str] = None
    ) -> tuple:
        """
         Updates a media file in the database and optionally replaces the physical file.

        Args:
            id (int): ID of the media file to update.
            type (Optional[str]): New type (e.g., image, video).
            title (Optional[str]): New title.
            file_content (Optional[bytes]): New file content if being updated.
            original_filename (Optional[str]): Original name of the new file.
            thumbnail_url (Optional[str]): New thumbnail URL.
            description (Optional[str]): New description.

        Returns:
            tuple: (status_code, message)
        """
        url = None
        MEDIA_DIR = "media/media_files"

        # Replace the file only if new content is provided
        if file_content and original_filename:
            os.makedirs(MEDIA_DIR, exist_ok=True)

            # Obtain the old media file details
            status_code, media = self.get_media_file(id)
            if status_code != STATUS_OK:
                return STATUS_BAD_REQUEST, {"message": "Previous media file not found"}

            old_url = media[0]["url"]
            old_path = old_url.replace("/media/media_files/", f"{MEDIA_DIR}/")

            if os.path.exists(old_path):
                os.remove(old_path)

            # Save the new file with a unique name
            extension = os.path.splitext(original_filename)[1]
            unique_name = f"{uuid.uuid4().hex}{extension}"
            new_path = os.path.join(MEDIA_DIR, unique_name)

            with open(new_path, "wb") as f:
                f.write(file_content)

            url = f"/media/media_files/{unique_name}"

        updated = self.media_queries.update_media_file(
            conn=self.conn,
            id=id,
            type=type,
            title=title,
            url=url,
            thumbnail_url=thumbnail_url,
            description=description,
            updated_by=self.updated_by
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
    
    def get_all_media_files(
            self, 
            collection_id: int, 
            limit: int = 10, 
            offset: int = 0, 
            search: Optional[str] = None
            ) -> tuple:
        """
        Retrieves all media files for a specific collection from the database.
        
        Args:
            collection_id (int): The ID of the collection to retrieve media files for.
            limit (int): The maximum number of media files to retrieve (default is 10).
            offset (int): The number of media files to skip before starting to collect the result set.
            search (Optional[str]): A search term to filter media files by title or description (default
        
        Returns:
            tuple: A tuple containing the status code and a list of media files or an error message.
        """
        all_media_files = self.media_queries.get_all_media_files(
            conn=self.conn,
            collection_id=collection_id,
            limit=limit,
            offset=offset,
            search=search
        )

        if not all_media_files:
            return STATUS_BAD_REQUEST, {"message": "No media files found for this collection"}

        return STATUS_OK, all_media_files
    