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
