from pydantic import BaseModel
from fastapi import UploadFile, File


class MicroplasticZoneForm(BaseModel):
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(
            ..., description="Microplastic zone file to be uploaded"
        ),
    ):
        return cls(
            file=file,
        )
