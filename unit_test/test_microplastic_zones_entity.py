import pytest
import io
from fastapi import UploadFile
from unittest.mock import MagicMock
from src.entities.microplastic_zones.microplastic_zones import MicroplasticZone
from src.entities.microplastic_zones.src.queries import MicroplasticZoneQueries
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST


@pytest.fixture
def mock_conn():
    mock = MagicMock()
    mock.executemany_insert.return_value = 1
    return mock


@pytest.fixture
def microplastic_zone(mock_conn):
    zone = MicroplasticZone(mock_conn)
    zone.microplastic_zone_queries = MicroplasticZoneQueries()
    return zone


@pytest.mark.asyncio
async def test_insert_microplastic_zone_success(microplastic_zone):
    csv_data = """polygon_id,geometry,NDVI,NDWI,NDCI,FDI,NDPI,pred_linear,pred_forest,pred_neural
1,"POLYGON((...))",0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8
"""
    upload_file = UploadFile(filename="test.csv", file=io.BytesIO(csv_data.encode()))

    microplastic_zone.microplastic_zone_queries.insert_microplastic_zone.__func__.query = (
        "INSERT INTO microplastic_zones VALUES (...)"
    )

    status, response = await microplastic_zone.insert_microplastic_zone(upload_file)

    assert status == STATUS_OK
    assert response["message"] == "Microplastic zone inserted successfully"
    microplastic_zone.conn.executemany_insert.assert_called_once()
    args = microplastic_zone.conn.executemany_insert.call_args[0]
    assert "INSERT INTO microplastic_zones" in args[0]
    assert isinstance(args[1], list)
    assert len(args[1]) == 1


@pytest.mark.asyncio
async def test_insert_microplastic_zone_failure(microplastic_zone):
    microplastic_zone.conn.executemany_insert.return_value = None
    csv_data = """polygon_id,geometry,NDVI,NDWI,NDCI,FDI,NDPI,pred_linear,pred_forest,pred_neural
2,"POLYGON((...))",0.11,0.21,0.31,0.41,0.51,0.61,0.71,0.81
"""
    upload_file = UploadFile(filename="test.csv", file=io.BytesIO(csv_data.encode()))

    microplastic_zone.microplastic_zone_queries.insert_microplastic_zone.__func__.query = (
        "INSERT INTO microplastic_zones VALUES (...)"
    )

    status, response = await microplastic_zone.insert_microplastic_zone(upload_file)

    assert status == STATUS_BAD_REQUEST
    assert response == "Failed to insert microplastic zone."
    microplastic_zone.conn.executemany_insert.assert_called_once()


@pytest.mark.asyncio
async def test_insert_microplastic_zone_invalid_csv(microplastic_zone):
    csv_data = "invalid_column\nvalue"
    upload_file = UploadFile(filename="bad.csv", file=io.BytesIO(csv_data.encode()))

    with pytest.raises(AttributeError):
        await microplastic_zone.insert_microplastic_zone(upload_file)
