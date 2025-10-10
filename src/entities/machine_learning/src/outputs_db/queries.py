from typing import Optional
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.query_reader import sql_query_reader
import os


base_dir = os.path.dirname(os.path.abspath(__file__))


class OutputsDBQueries:
    @sql_query_reader(base_dir, "outputs_db_post.sql")
    def insert_outputs(self, batch: list, conn: DatabaseConnection) -> Optional[int]:
        """
        Inserts a new output into the database.

        Args:
            batch (list): A list of tuples containing output data.
            conn (DatabaseConnection): The database connection object.

        Returns:
            Optional[int]: The ID of the inserted output, or None if the insertion failed.
        """

        query: str = self.insert_outputs.query
        resp = conn.executemany_insert(query, batch)
        return resp
