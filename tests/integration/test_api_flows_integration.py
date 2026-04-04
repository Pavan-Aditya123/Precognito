import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_ingest_and_get_assets_flow(auth_client: AsyncClient, mocker):
    """
    Integration test: Ingest data via /ingest/dev and verify it can be retrieved.
    This tests the integration between the API router, ingestion core, and InfluxDB client.
    """
    # 1. Mock the InfluxDB save functions
    mock_save = mocker.patch("precognito.ingestion.influx_client.write_api.write")
    
    # 2. Ingest some dev data
    telemetry_data = {
        "device_id": "test_motor_01",
        "temperature": 45.5,
        "vibration": 0.02
    }
    
    response = await auth_client.post("/ingest/dev", json=telemetry_data)
    
    # Verify the response from the integrated endpoint
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert mock_save.called

    # 3. Mock the InfluxDB query for assets
    mock_query = mocker.patch("precognito.ingestion.influx_client.query_api.query")
    
    # Mock records for the /assets endpoint
    mock_record = mocker.Mock()
    mock_record.values = {"device_id": "test_motor_01"}
    mock_record.get_time.return_value = mocker.Mock(isoformat=lambda: "2026-04-04T12:00:00Z")
    
    mock_table = mocker.Mock(records=[mock_record])
    mock_query.return_value = [mock_table]

    # 4. Fetch assets and verify the data is integrated
    response = await auth_client.get("/assets")
    
    assert response.status_code == 200
    assets = response.json()
    assert len(assets) > 0
    assert assets[0]["id"] == "test_motor_01"

@pytest.mark.asyncio
async def test_unauthorized_access_integration(client: AsyncClient):
    """
    Verify that security middleware is integrated and active for protected routes.
    """
    # Attempt to access admin logs without auth
    response = await client.get("/audit-logs")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
