"""
API router for managing audit logs and maintenance records.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from precognito.work_orders.database import SessionLocal
from precognito.work_orders.models import Audit

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
        remarks=data.get("remarks")
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
