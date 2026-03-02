from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, PRED_FOREST
from src.entities.machine_learning.src.outputs_db.queries import OutputsDBQueries
from src.shared.db_config import DatabaseConnection
from typing import Tuple, Union
from datetime import datetime, date
import pandas as pd
import io


def _to_datetime(created_at: Union[str, datetime, date]) -> datetime:
    """Convierte la fecha pasada a datetime para guardar en created_at."""
    if isinstance(created_at, datetime):
        return created_at
    if isinstance(created_at, date) and not isinstance(created_at, datetime):
        return datetime.combine(created_at, datetime.min.time())
    if isinstance(created_at, str):
        # Acepta "YYYY-MM-DD" o "YYYY-MM-DD HH:MM:SS"
        created_at = created_at.strip()
        if len(created_at) <= 10:
            return datetime.strptime(created_at, "%Y-%m-%d")
        return datetime.strptime(created_at[:19], "%Y-%m-%d %H:%M:%S")
    raise TypeError("created_at debe ser str, date o datetime")


class OutputsDB:
    def __init__(self):
        self.outputs_db = OutputsDBQueries()
        self.conn = DatabaseConnection()

    def insert_outputs(
        self, file_path: str, created_at: Union[str, datetime, date]
    ) -> Tuple[int, str]:
        """
        Inserts a new output into the database.

        Args:
            file_path: Ruta del CSV con las predicciones.
            created_at: Fecha a guardar en created_at (str 'YYYY-MM-DD', date o datetime).

        Returns:
            tuple: (código de estado, mensaje).
        """
        created_at_dt = _to_datetime(created_at)
        df = self.read_predictions_csv(file_path)
        batch = []
        for row in df.itertuples(index=False):
            if float(row.pred_forest) > PRED_FOREST:
                batch.append(
                    (
                        int(row.polygon_id),
                        row.geometry,
                        float(row.NDVI),
                        float(row.NDWI),
                        float(row.NDCI),
                        float(row.FDI),
                        float(row.NDPI),
                        float(row.BLUE),
                        float(row.GREEN),
                        float(row.RED),
                        float(row.REDEDGE1),
                        float(row.REDEDGE2),
                        float(row.REDEDGE3),
                        float(row.NIR_10m),
                        float(row.NIR_20m),
                        float(row.SWIR1),
                        float(row.SWIR2),
                        float(row.pred_linear),
                        float(row.pred_forest),
                        float(row.pred_neural),
                        created_at_dt,
                    )
                )
        resp = self.outputs_db.insert_outputs(batch, self.conn)
        if resp is None:
            return STATUS_BAD_REQUEST, {
                "message": "Error inserting output",
                "status": False,
            }

        return STATUS_OK, {
            "message": "Output inserted successfully",
            "status": resp,
        }

    def read_predictions_csv(self, file_path: str) -> pd.DataFrame:
        cleaned_lines = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i == 0:
                    cleaned_lines.append(line.lstrip("\ufeff"))
                else:
                    core = line.rstrip("\n\r")
                    if len(core) >= 2 and core[0] == '"' and core[-1] == '"':
                        core = core[1:-1]
                        core = core.replace('""', '"')
                    cleaned_lines.append(core + "\n")

        buf = io.StringIO("".join(cleaned_lines))
        df = pd.read_csv(buf, sep=",", quotechar='"', engine="python")

        df["polygon_id"] = df["polygon_id"].astype(int)
        numeric_cols = [
            "NDVI",
            "NDWI",
            "NDCI",
            "FDI",
            "NDPI",
            "BLUE",
            "GREEN",
            "RED",
            "REDEDGE1",
            "REDEDGE2",
            "REDEDGE3",
            "NIR_10m",
            "NIR_20m",
            "SWIR1",
            "SWIR2",
            "pred_linear",
            "pred_forest",
            "pred_neural",
        ]
        for c in numeric_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        return df
