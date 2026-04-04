import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_sql_injection_attempt(auth_client: AsyncClient):
    """
    Test for SQL injection vulnerability on an endpoint that takes string input.
    """
    import random
    rand_id = random.randint(10000, 99999)
    # SQL Injection payload in assetId
    payload = {
        "assetId": f"PUMP_SQLI_{rand_id}'; DROP TABLE assets; --",
        "assetName": "Malicious Pump",
        "assetType": "pump"
    }
    
    response = await auth_client.post("/work-orders/assets/", json=payload)
    
    # We expect either a 200 (if it safely handled the string) or a 422/400.
    # The key is that the DROP TABLE didn't happen and the app didn't 500 due to syntax error.
    assert response.status_code in [200, 400, 422]

@pytest.mark.asyncio
async def test_xss_injection_attempt(auth_client: AsyncClient, mocker):
    """
    Test for XSS vulnerability in feedback details.
    """
    from precognito.api import app
    
    payload = {
        "anomalyId": "123",
        "deviceId": "motor_1",
        "isReal": True,
        "details": "<script>alert('XSS')</script>"
    }
    
    # Mock the database pool if not present (sometimes TestClient setup is tricky)
    if not hasattr(app, "db_pool"):
        app.db_pool = MagicMock()
        
    mock_conn = AsyncMock()
    app.db_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mocker.patch("precognito.api.log_audit_action")
    
    response = await auth_client.post("/analytics/feedback", json=payload)
    # Should either succeed (ignoring extra fields) or 422. 500 is failure.
    assert response.status_code in [200, 400, 422]

@pytest.mark.asyncio
async def test_auth_token_tampering(client: AsyncClient):
    """
    Test auth bypass with tampered token.
    """
    from precognito.api import app
    
    if not hasattr(app, "db_pool"):
        app.db_pool = MagicMock()
        
    mock_conn = AsyncMock()
    app.db_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mock_conn.fetchrow.return_value = None # No session found
    
    headers = {"Authorization": "Bearer invalidated-token-123"}
    response = await client.get("/audit-logs", headers=headers)
    
    # Should be rejected with 401
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_cors_bypass_attempt(client: AsyncClient):
    """
    Test CORS origin restriction.
    """
    headers = {"Origin": "http://evil-domain.com"}
    response = await client.options("/health", headers=headers)
    
    # Check that the origin is not in the allowed list
    if "access-control-allow-origin" in response.headers:
        assert response.headers["access-control-allow-origin"] != "http://evil-domain.com"
