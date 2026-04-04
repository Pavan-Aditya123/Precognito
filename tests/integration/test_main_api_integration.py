import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_main_api_get_anomalies(auth_client: AsyncClient, mocker):
    """Integration test for InfluxDB anomaly retrieval."""
    mock_query = mocker.patch("precognito.ingestion.influx_client.query_api.query")
    
    mock_record = mocker.Mock()
    mock_record.values = {"device_id": "test_dev", "severity": "HIGH", "reason": "Test Anomaly"}
    mock_record.get_time.return_value = datetime.now(timezone.utc)
    
    mock_query.return_value = [mocker.Mock(records=[mock_record])]

    response = await auth_client.get("/anomalies")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["severity"] == "HIGH"

@pytest.mark.asyncio
async def test_safety_alerts_and_heartbeats(auth_client: AsyncClient, mocker):
    """Integration test for safety alerts and persistent heartbeats."""
    mock_query = mocker.patch("precognito.ingestion.influx_client.query_api.query")
    
    # Mock for alerts
    mock_record = mocker.Mock()
    mock_record.values = {"device_id": "test_dev", "type": "THERMAL", "temperature": 85.0}
    mock_record.get_time.return_value = datetime.now(timezone.utc)
    
    mock_query.return_value = [mocker.Mock(records=[mock_record])]

    response = await auth_client.get("/safety-alerts")
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    # Mock for heartbeats
    response = await auth_client.get("/heartbeats")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_feedback_loop_integration(auth_client: AsyncClient, mocker):
    """Integration test for the feedback loop and metrics calculation."""
    from precognito.api import app
    
    # 1. Submit feedback
    feedback_data = {
        "anomalyId": "123-test",
        "deviceId": "motor_1",
        "isReal": True
    }
    
    # Setup database mocks for submit_feedback
    mock_conn = AsyncMock()
    app.db_pool.acquire.return_value.__aenter__.return_value = mock_conn
    
    response = await auth_client.post("/analytics/feedback", json=feedback_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert mock_conn.execute.called

    # 2. Get metrics
    # Mock InfluxDB count
    mocker.patch("precognito.ingestion.influx_client.get_total_telemetry_count", return_value=10000)
    
    # Mock Postgres counts (fetchval returns integers)
    mock_conn.fetchval.side_effect = [5, 2] # true_positives, false_positives
    
    response = await auth_client.get("/analytics/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["truePositives"] == 5
    assert data["falsePositives"] == 2
    assert data["trueNegatives"] == 10000 - (5 + 2)
    assert "precision" in data
    assert "accuracy" in data
    assert "fdr" in data
    assert data["accuracy"] > 0
