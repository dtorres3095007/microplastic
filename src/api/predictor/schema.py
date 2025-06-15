from pydantic import BaseModel, Field
from typing import List

class Polygon(BaseModel):
    type: str = Field(..., example="Polygon", description="GeoJSON geometry type")
    coordinates: List[List[List[float]]] = Field(
        ...,
        example=[
            [
                [-73.35831397455212, 11.886251690628882],
                [-73.35831397455212, 11.884186337143731],
                [-73.35651477436537, 11.884186337143731],
                [-73.35651477436537, 11.886251690628882],
                [-73.35831397455212, 11.886251690628882]
            ]
        ],
        description="Polygon coordinates as a list of linear rings"
    )

class PredictorRequestBody(BaseModel):
    initial_date: str = Field(..., example="2025-03-15", description="Start date for satellite image data")
    end_date: str = Field(..., example="2025-03-16", description="End date for satellite image data")
    location: Polygon
