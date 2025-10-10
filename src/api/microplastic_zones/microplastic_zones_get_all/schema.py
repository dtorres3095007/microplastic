from pydantic import BaseModel, Field


class MicroplasticZonesQueryParams(BaseModel):
    limit: int = Field(
        default=10, gt=0, description="Maximum number of microplastic zones to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of microplastic zones to skip before starting to collect the result set",
    )
