from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.microplastic_zones.src.queries import MicroplasticZoneQueries
from src.shared.db_config import DatabaseConnection
from typing import Tuple
from fastapi import UploadFile
import pandas as pd
import io


class MicroplasticZone:
    def __init__(self, conn: DatabaseConnection):
        self.microplastic_zone_queries = MicroplasticZoneQueries()
        self.conn = conn

    async def insert_microplastic_zone(self, file: UploadFile) -> Tuple[int, str]:
        """
        Inserts a new microplastic zone into the database.

        Args:
            file (UploadFile): The file containing microplastic zone data.

        Returns:
            tuple: A tuple containing the status code and a message.
        """
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        batch = []
        for row in df.itertuples(index=False):
            batch.append(
                (
                    int(row.polygon_id),
                    row.geometry,
                    float(row.NDVI),
                    float(row.NDWI),
                    float(row.NDCI),
                    float(row.FDI),
                    float(row.NDPI),
                    float(row.pred_linear),
                    float(row.pred_forest),
                    float(row.pred_neural),
                )
            )
        resp = self.microplastic_zone_queries.insert_microplastic_zone(batch, self.conn)
        if resp is None:
            return STATUS_BAD_REQUEST, "Failed to insert microplastic zone."

        return STATUS_OK, {
            "message": "Microplastic zone inserted successfully",
            "status": resp,
        }
