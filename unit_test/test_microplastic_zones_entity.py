import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import UploadFile
from src.entities.microplastic_zones.microplastic_zones import MicroplasticZone
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST

@pytest.fixture
def db_conn():
    return MagicMock()

@pytest.fixture
def microplastic_zone(db_conn):
    return MicroplasticZone(db_conn)

@pytest.mark.asyncio
async def test_insert_microplastic_zone_ok(microplastic_zone):
    # Mock UploadFile
    csv_content = (
        "polygon_id,geometry,NDVI,NDWI,NDCI,FDI,NDPI,pred_linear,pred_forest,pred_neural\n"
        "1,POLYGON((...)),0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8\n"
    )
    mock_file = MagicMock(spec=UploadFile)
    mock_file.read = AsyncMock(return_value=csv_content.encode())

    # Patch insert_microplastic_zone to return a status
    with patch.object(microplastic_zone.microplastic_zone_queries, "insert_microplastic_zone", return_value=1):
        status, msg = await microplastic_zone.insert_microplastic_zone(mock_file)
    assert status == STATUS_OK
    assert msg["message"] == "Microplastic zone inserted successfully"
    assert msg["status"] == 1

@pytest.mark.asyncio
async def test_insert_microplastic_zone_fail(microplastic_zone):
    csv_content = (
        "polygon_id,geometry,NDVI,NDWI,NDCI,FDI,NDPI,pred_linear,pred_forest,pred_neural\n"
        "1,POLYGON((...)),0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8\n"
    )
    mock_file = MagicMock(spec=UploadFile)
    mock_file.read = AsyncMock(return_value=csv_content.encode())

    # Patch insert_microplastic_zone to return None (simulate failure)
    with patch.object(microplastic_zone.microplastic_zone_queries, "insert_microplastic_zone", return_value=None):
        status, msg = await microplastic_zone.insert_microplastic_zone(mock_file)
    assert status == STATUS_BAD_REQUEST
    assert msg == "Failed to insert microplastic zone."