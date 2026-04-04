import pytest
import random
from httpx import AsyncClient
from precognito.work_orders.database import SessionLocal
from precognito.inventory import models

@pytest.fixture
def test_part():
    """Create a test part in the database."""
    db = SessionLocal()
    # Use random number to avoid UNIQUE constraint violation across multiple tests
    rand_id = random.randint(1000, 9999)
    part = models.Inventory(
        partName=f"Test Bearing {rand_id}",
        partNumber=f"BRG-{rand_id}",
        quantity=50,
        minThreshold=10,
        leadTimeDays=5,
        costPerUnit=25.50,
        category="Bearings"
    )
    db.add(part)
    db.commit()
    db.refresh(part)
    part_id = part.id
    db.close()
    return part_id

@pytest.mark.asyncio
async def test_inventory_reserve_and_po(auth_client: AsyncClient, test_part):
    """
    Integration test for inventory reservation and purchase orders.
    """
    # 1. Reserve Part
    reserve_data = {
        "partId": test_part,
        "quantity": 5,
        "workOrderId": 999
    }
    response = await auth_client.post("/inventory/reserve", json=reserve_data)
    assert response.status_code == 200
    assert response.json()["status"] == "reserved"

    # 2. Verify deduction
    response = await auth_client.get("/inventory/")
    assert response.status_code == 200
    # Find our part
    parts = response.json()
    part = next(p for p in parts if p["id"] == test_part)
    assert part["quantity"] == 45

    # 3. Create Purchase Order
    po_data = {
        "partId": test_part,
        "quantity": 20
    }
    response = await auth_client.post("/inventory/purchase-order", json=po_data)
    assert response.status_code == 200
    assert response.json()["status"] == "PO_GENERATED"
    assert response.json()["quantity"] == 20

@pytest.mark.asyncio
async def test_jit_alerts_integration(auth_client: AsyncClient, test_part, mocker):
    """
    Integration test for JIT alerts based on InfluxDB RUL forecasts.
    """
    # 1. Mock InfluxDB to return low RUL for a device
    mocker.patch("precognito.ingestion.influx_client.get_all_devices", return_value=["DEVICE_X"])
    mock_query = mocker.patch("precognito.inventory.api.query_latest_data")
    
    mock_record = mocker.Mock()
    mock_record.get_field.return_value = "predicted_rul_hours"
    mock_record.get_value.return_value = 10.0 # 10h RUL < 5 day lead time (120h)
    mock_query.return_value = [mocker.Mock(records=[mock_record])]

    # 2. Check JIT alerts
    response = await auth_client.get("/inventory/jit-alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) > 0
    assert alerts[0]["deviceId"] == "DEVICE_X"
    assert alerts[0]["priority"] == "CRITICAL"
