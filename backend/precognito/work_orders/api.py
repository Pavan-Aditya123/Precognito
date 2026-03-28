from fastapi import APIRouter

router=APIRouter()

workorders = [
    {
        "id": 1,
        "machine_id": "M101",
        "issue": "High vibration",
        "priority": "HIGH",
        "status": "PENDING",
        "assigned_to": None
    }
]

@router.get("/workorders")
def get_workorders():
    return workorders
