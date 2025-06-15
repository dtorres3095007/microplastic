from pydantic import BaseModel, Field


class MediaFileSchema(BaseModel):
    collection_id: str = Field(..., description="The ID of the collection to which the media file belongs.")
    type: str = Field(..., example="image", description="The type of the media file (e.g., 'image', 'video').")
    title: str = Field(..., example="Titulo de prueba...", description="The title of the media file.")
    url: str = Field(..., example="/media/media_files/imagen.jpg", description="The URL of the media file.")
    thumbnail_url: str = Field(None, description="The URL of the thumbnail image for the media file.")
    description: str = Field(None, description="A description of the media file.")
    