"""
SQLAlchemy models for assets, audits, and technician rosters.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from precognito.work_orders.database import Base
from datetime import datetime

class Asset(Base):
    """Represents an industrial asset or machine.

    Attributes:
        id (int): Primary key.
        assetId (str): Unique identifier for the asset.
        assetName (str): Human-readable name of the asset.
        manual (str): URL or reference to the asset manual.
        mttr (str): Mean Time To Repair.
    """
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    assetId = Column(String, unique=True, index=True)
    assetName = Column(String)
    manual = Column(String)
    mttr = Column(String)

class Audit(Base):
    """Represents a maintenance audit or work order record.

    Attributes:
        id (int): Primary key.
        assetId (str): ID of the asset being audited.
        status (str): Current status of the work order (e.g., OPEN, CLOSED).
        remarks (str): Description or notes about the maintenance activity.
        timestamp (datetime): When the audit record was created.
        assignedTo (str): ID of the technician assigned to the task.
    """
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    assetId = Column(String, index=True)
    status = Column(String)
    remarks = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    assignedTo = Column(String, index=True) # User ID of technician

class Roster(Base):
    """Represents a technician's availability and skill set.

    Attributes:
        id (int): Primary key.
        userId (str): ID of the user (technician).
        status (str): Current availability (AVAILABLE, ON_LEAVE, BUSY).
        shift (str): Assigned shift (DAY, NIGHT).
        skills (str): Technician skills (MECHANICAL, ELECTRICAL, GENERAL).
        lastAssigned (datetime): Timestamp of the last assigned task.
    """
    __tablename__ = "roster"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, index=True)
    status = Column(String, default="AVAILABLE") # AVAILABLE, ON_LEAVE, BUSY
    shift = Column(String) # DAY, NIGHT
    skills = Column(String) # MECHANICAL, ELECTRICAL, GENERAL
    lastAssigned = Column(DateTime)
