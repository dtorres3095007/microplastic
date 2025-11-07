from typing import Optional
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.query_reader import sql_query_reader
import os


base_dir = os.path.dirname(os.path.abspath(__file__))


class MicroplasticZoneQueries:
    @sql_query_reader(base_dir, "microplastic_zones_post.sql")
    def insert_microplastic_zone(
        self, batch: list, conn: DatabaseConnection
    ) -> Optional[int]:
        """
        Inserts a new microplastic zone into the database.

        Args:
            batch (list): A list of tuples containing microplastic zone data.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the inserted microplastic zone, or None if the insertion failed.
        """

        query: str = self.insert_microplastic_zone.query
        resp = conn.executemany_insert(query, batch)
        return resp

    @sql_query_reader(base_dir, "microplastic_zones_get_all.sql")
    def get_all_microplastic_zones(
        self,
        limit: int,
        offset: int,
        pred_min: float | None,
        pred_max: float | None,
        month: int | None,
        year: int | None,
        conn: DatabaseConnection,
    ) -> Optional[list]:
        """
        Retrieves all microplastic zones from the database.

        Args:
            limit (int): The maximum number of microplastic zones to retrieve.
            offset (int): The number of microplastic zones to skip before starting to collect the result set.
            pred_min (float): Minimum predicted microplastic concentration to filter results.
            pred_max (float): Maximum predicted microplastic concentration to filter results.
            month (int): Month to filter results.
            year (int): Year to filter results.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[list]: A list of microplastic zones, or None if the retrieval failed.
        """
        query: str = self.get_all_microplastic_zones.query
        resp = conn.execute_query(
            query,
            {
                "limit": limit,
                "offset": offset,
                "pred_min": pred_min,
                "pred_max": pred_max,
                "month": month,
                "year": year,
            },
        )
        return resp

    @sql_query_reader(base_dir, "microplastic_zones_get_dates.sql")
    def get_dates_microplastic_zones(
        self,
        conn: DatabaseConnection,
    ) -> Optional[list]:
        """
        Retrieves available dates for microplastic zones from the database.

        Args:
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[list]: A list of available dates, or None if the retrieval failed.
        """
        query: str = self.get_dates_microplastic_zones.query
        resp = conn.execute_query(
            query,
        )
        return resp
