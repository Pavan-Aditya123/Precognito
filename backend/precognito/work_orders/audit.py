"""
API router for managing audit logs and maintenance records.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from precognito.work_orders.database import SessionLocal
from precognito.work_orders.models import Audit, Asset
from precognito.inventory.models import Inventory

router = APIRouter(prefix="/audit", tags=["Audit"])


def get_db():
    """Dependency to get a SQLAlchemy database session.

    Yields:
        Session: A database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE audit log
@router.post("/")
def create_audit(data: dict, db: Session = Depends(get_db)):
    """Creates a new audit log entry.

    Args:
        data (dict): Dictionary containing audit details (assetId, status, remarks).
        db (Session): Database session dependency.

    Returns:
        Audit: The newly created Audit object.
    """
    audit = Audit(
        assetId=data["assetId"],
        status=data["status"],
        remarks=data.get("remarks"),
        assignedTo=data.get("assignedTo")
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


# GET all audits
@router.get("/")
def get_audits(db: Session = Depends(get_db)):
    """Retrieves all audit logs from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        list: A list of all Audit objects.
    """
    return db.query(Audit).all()

@router.get("/{asset_id}")
def get_audit_by_asset(asset_id: str, db: Session = Depends(get_db)):
    """Retrieves all audit logs for a specific asset.

    Args:
        asset_id (str): The unique identifier of the asset.
        db (Session): Database session dependency.

    Returns:
        list: A list of Audit objects for the specified asset.
    """
    return db.query(Audit).filter(Audit.assetId == asset_id).all()

@router.patch("/{audit_id}/complete")
def complete_work_order(audit_id: int, data: dict, db: Session = Depends(get_db)):
    """Finalizes a work order, deducting parts and calculating costs.

    Args:
        audit_id (int): The ID of the work order to complete.
        data (dict): Completion details (resolution, partId, quantityUsed, laborHours).
        db (Session): Database session dependency.

    Returns:
        dict: Success status and finalized cost.
    """
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    resolution = data.get("resolution", "No notes provided")
    part_id = data.get("partId")
    qty = data.get("quantityUsed", 0)
    labor_hours = data.get("laborHours", 2.0) # Default 2 hours if not specified
    
    total_parts_cost = 0.0
    
    # 1. Process Inventory if part used
    if part_id and qty > 0:
        part = db.query(Inventory).filter(Inventory.id == part_id).first()
        if not part:
            raise HTTPException(status_code=404, detail="Part not found in inventory")
        
        if part.quantity < qty:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {part.partName}")
            
        part.quantity -= qty
        total_parts_cost = float(part.costPerUnit) * qty
    
    # 2. Calculate Labor Cost (Prototype rate: $80/hr)
    labor_cost = labor_hours * 80.0
    actual_cost = total_parts_cost + labor_cost
    
    # 3. Update Work Order
    audit.status = "COMPLETED"
    audit.resolution = resolution
    audit.partId = part_id
    audit.quantityUsed = qty
    audit.actualCost = actual_cost
    audit.completedAt = datetime.now(timezone.utc)
    
    db.commit()
    
    return {
        "status": "success",
        "workOrderId": audit.id,
        "actualCost": actual_cost,
        "message": f"Work order completed. Total cost: ${actual_cost:.2f}"
    }
