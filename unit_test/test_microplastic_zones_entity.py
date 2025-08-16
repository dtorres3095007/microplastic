import pytest
import io
import pandas as pd
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile
from src.entities.microplastic_zones.microplastic_zones import MicroplasticZone
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST


@pytest.mark.asyncio
async def test_insert_microplastic_zone_success():
    # Create a CSV in memory
    csv_data = """polygon_id,geometry,NDVI,NDWI,NDCI,FDI,NDPI,pred_linear,pred_forest,pred_neural
    1,"POLYGON((...))",0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8
    """
    upload_file = UploadFile(filename="test.csv", file=io.BytesIO(csv_data.encode()))

    # Mock of DatabaseConnection
    mock_conn = MagicMock()

    # Mock of MicroplasticZoneQueries
    mock_queries = MagicMock()
    mock_queries.insert_microplastic_zone.return_value = True

    # Instance of MicroplasticZone with mock
    zone = MicroplasticZone(mock_conn)
    zone.microplastic_zone_queries = mock_queries

    status, response = await zone.insert_microplastic_zone(upload_file)

    assert status == STATUS_OK
    assert response["message"] == "Microplastic zone inserted successfully"
    assert response["status"] is True
    mock_queries.insert_microplastic_zone.assert_called_once()
    assert isinstance(mock_queries.insert_microplastic_zone.call_args[0][0], list)
    assert len(mock_queries.insert_microplastic_zone.call_args[0][0]) == 1


@pytest.mark.asyncio
async def test_insert_microplastic_zone_failure():
    csv_data = """polygon_id,geometry,NDVI,NDWI,NDCI,FDI,NDPI,pred_linear,pred_forest,pred_neural
    2,"POLYGON((...))",0.11,0.21,0.31,0.41,0.51,0.61,0.71,0.81
    """
    upload_file = UploadFile(filename="test.csv", file=io.BytesIO(csv_data.encode()))

    mock_conn = MagicMock()
    mock_queries = MagicMock()
    mock_queries.insert_microplastic_zone.return_value = None

    zone = MicroplasticZone(mock_conn)
    zone.microplastic_zone_queries = mock_queries

    status, response = await zone.insert_microplastic_zone(upload_file)

    assert status == STATUS_BAD_REQUEST
    assert response == "Failed to insert microplastic zone."
    mock_queries.insert_microplastic_zone.assert_called_once()


@pytest.mark.asyncio
async def test_insert_microplastic_zone_invalid_csv(monkeypatch):
    # Csv without required columns
    csv_data = "invalid_column\nvalue"
    upload_file = UploadFile(filename="bad.csv", file=io.BytesIO(csv_data.encode()))

    mock_conn = MagicMock()
    mock_queries = MagicMock()

    zone = MicroplasticZone(mock_conn)
    zone.microplastic_zone_queries = mock_queries

    with pytest.raises(AttributeError):  # Because expected columns are missing
        await zone.insert_microplastic_zone(upload_file)
