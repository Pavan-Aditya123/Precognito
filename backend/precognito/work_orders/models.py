from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from precognito.work_orders.database import Base
from datetime import datetime

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    assetId = Column(String, unique=True, index=True)
    assetName = Column(String)
    manual = Column(String)
    mttr = Column(String)

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    assetId = Column(String, index=True)
    status = Column(String)
    remarks = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    assignedTo = Column(String, index=True) # User ID of technician

class Roster(Base):
    __tablename__ = "roster"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, index=True)
    status = Column(String, default="AVAILABLE") # AVAILABLE, ON_LEAVE, BUSY
    shift = Column(String) # DAY, NIGHT
    skills = Column(String) # MECHANICAL, ELECTRICAL, GENERAL
    lastAssigned = Column(DateTime)
