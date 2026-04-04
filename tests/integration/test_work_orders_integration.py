import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_work_order_full_lifecycle(auth_client: AsyncClient):
    """
    Integration test for the complete work order lifecycle:
    Create Asset -> Create Audit -> Get Audit -> Complete Work Order.
    """
    import random
    rand_id = random.randint(1000, 9999)
    asset_id = f"PUMP_{rand_id}"

    # 1. Create Asset
    asset_data = {
        "assetId": asset_id,
        "assetName": "Main Coolant Pump",
        "assetType": "pump",
        "manual": "http://manuals.com/pump1.pdf",
        "mttr": "2.5h"
    }
    response = await auth_client.post("/work-orders/assets/", json=asset_data)
    assert response.status_code == 200
    assert response.json()["assetId"] == asset_id

    # 2. Create Audit (Work Order)
    audit_data = {
        "assetId": asset_id,
        "status": "PENDING",
        "remarks": "Scheduled maintenance check",
        "assignedTo": "tech_alpha"
    }
    response = await auth_client.post("/work-orders/audit/", json=audit_data)
    assert response.status_code == 200
    audit_id = response.json()["id"]
    assert response.json()["assetId"] == asset_id

    # 3. Get Audits for Asset
    response = await auth_client.get(f"/work-orders/audit/{asset_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["id"] == audit_id

    # 4. Complete Work Order
    complete_data = {
        "resolution": "Seal replaced, tested successfully.",
        "partId": None,
        "quantityUsed": 0,
        "laborHours": 1.5
    }
    response = await auth_client.patch(f"/work-orders/audit/{audit_id}/complete", json=complete_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["actualCost"] > 0
