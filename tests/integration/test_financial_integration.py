import pytest
from datetime import datetime, timezone
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_financial_reporting_integration(auth_client: AsyncClient, mocker):
    """
    Integration test for financial recommendations and ROI calculations.
    """
    # 1. Mock InfluxDB for recommendations
    mock_query = mocker.patch("precognito.financial.services.query_latest_data")
    
    mock_record = mocker.Mock()
    # Mock multiple fields correctly for fetch_real_rul_and_prob
    mock_record.get_field.side_effect = ["predicted_rul_hours", "confidence"]
    mock_record.get_value.side_effect = [50.0, 0.85]
    
    mock_query.return_value = [mocker.Mock(records=[mock_record])]

    # 2. Get recommendations
    response = await auth_client.get("/admin-reporting/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    # Our mocked values (RUL=50h) lead to "Schedule Repair soon" which has "Cost avoided"
    assert "Cost avoided" in data["recommendations"][0]["explanation"]

@pytest.mark.asyncio
async def test_system_health_endpoint(auth_client: AsyncClient):
    """
    Integration test for system health monitoring.
    """
    response = await auth_client.get("/admin-reporting/health")
    assert response.status_code == 200
    assert response.json()["status"] == "Healthy"
    assert "cpu_usage_percent" in response.json()

@pytest.mark.asyncio
async def test_audit_report_endpoint(auth_client: AsyncClient):
    """
    Integration test for compliance audit reports.
    """
    # The route is /admin-reporting/audit
    response = await auth_client.get("/admin-reporting/audit")
    assert response.status_code == 200
    assert "total_logs" in response.json()
