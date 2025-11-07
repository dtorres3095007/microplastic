from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.microplastic_zones.src.queries import MicroplasticZoneQueries
from src.shared.db_config import DatabaseConnection
from typing import Tuple
from fastapi import UploadFile
import pandas as pd
import io
from src.shared.constants import MONTHS_ES
from datetime import datetime
import calendar


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

    async def get_all_microplastic_zones(
        self,
        limit: int,
        offset: int,
        pred_min: float | None,
        pred_max: float | None,
        month: int | None,
        year: int | None,
        month_year: str | None,
    ) -> Tuple[int, str]:
        """
        Retrieves all microplastic zones from the database.

        Args:
            limit (int): Maximum number of microplastic zones to return.
            offset (int): Number of microplastic zones to skip before starting to collect the result set.
            pred_min (float): Minimum predicted microplastic concentration to filter results.
            pred_max (float): Maximum predicted microplastic concentration to filter results.
            month (int): Month to filter results.
            year (int): Year to filter results.
            month_year (str): Month and year to filter results, in the format 'mes año'.

        Returns:
            tuple: A tuple containing the status code and a list of microplastic zones.
        """
        start, end = self.get_rank_dates(month_year)
        resp = self.microplastic_zone_queries.get_all_microplastic_zones(
            conn=self.conn,
            limit=limit,
            offset=offset,
            pred_min=pred_min,
            pred_max=pred_max,
            month=month,
            year=year,
            start=start,
            end=end,
        )
        if resp is None:
            return STATUS_BAD_REQUEST, "Failed to retrieve microplastic zones."

        return STATUS_OK, resp

    async def get_dates_microplastic_zones(self) -> Tuple[int, str]:
        """
        Retrieves available dates for microplastic zones from the database.

        Returns:
            tuple: A tuple containing the status code and a list of available dates.
        """
        resp = self.microplastic_zone_queries.get_dates_microplastic_zones(
            conn=self.conn,
        )
        if resp is None:
            return STATUS_BAD_REQUEST, "Failed to retrieve microplastic zone dates."

        for row in resp:
            month = MONTHS_ES[row["month"] - 1]
            row["month_year_label"] = f"{month} {row['year']}"

        return STATUS_OK, resp

    def get_rank_dates(self, month_year: str):
        month_es = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12,
        }

        parts = month_year.lower().split()
        month = month_es[parts[0]]
        year = int(parts[1])

        start = datetime(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end = datetime(year, month, last_day, 23, 59, 59)

        return start, end
