"""
API router for managing industrial assets.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from precognito.work_orders.database import SessionLocal
from precognito.work_orders.models import Asset

router = APIRouter(prefix="/assets", tags=["Assets"])


# DB dependency
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


# GET all assets
@router.get("/")
def get_assets(db: Session = Depends(get_db)):
    """Retrieves all assets from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        list: A list of all Asset objects.
    """
    return db.query(Asset).all()


# CREATE asset
@router.post("/")
def create_asset(data: dict, db: Session = Depends(get_db)):
    """Creates a new asset in the database.

    Args:
        data (dict): Dictionary containing asset details (assetId, assetName, 
                     manual, mttr).
        db (Session): Database session dependency.

    Returns:
        Asset: The newly created Asset object.
    """
    asset = Asset(
        assetId=data["assetId"],
        assetName=data["assetName"],
        manual=data.get("manual"),
        mttr=data.get("mttr"),
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
