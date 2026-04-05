from pydantic import BaseModel, Field
from typing import Optional

class AssetCreateRequest(BaseModel):
    """Schema for creating a new industrial asset.

    Attributes:
        assetId (str): Unique identifier for the asset.
        assetName (str): Human-readable name of the asset.
        manual (Optional[str]): URL or path to asset manual.
        mttr (Optional[str]): Mean Time To Repair (e.g., '2.5h').
    """
    assetId: str = Field(..., description="Unique identifier for the asset")
    assetName: str = Field(..., description="Human-readable name of the asset")
    manual: Optional[str] = Field(None, description="URL or path to asset manual")
    mttr: Optional[str] = Field(None, description="Mean Time To Repair (e.g., '2.5h')")

class AuditCreateRequest(BaseModel):
    """Schema for creating a new audit log or work order.

    Attributes:
        assetId (str): ID of the asset being audited.
        status (str): Status of the audit (e.g., 'PENDING', 'IN_PROGRESS').
        remarks (Optional[str]): Additional audit remarks.
        assignedTo (Optional[str]): ID of the user assigned to this work order.
    """
    assetId: str = Field(..., description="ID of the asset being audited")
    status: str = Field(..., description="Status of the audit (e.g., 'PENDING', 'IN_PROGRESS')")
    remarks: Optional[str] = Field(None, description="Additional audit remarks")
    assignedTo: Optional[str] = Field(None, description="ID of the user assigned to this work order")

class WorkOrderCompleteRequest(BaseModel):
    """Schema for completing a work order with parts and labor details.

    Attributes:
        resolution (str): Description of the fix/resolution.
        partId (Optional[int]): ID of the part used from inventory.
        quantityUsed (int): Quantity of the part used.
        laborHours (float): Total labor hours spent.
    """
    resolution: str = Field(..., description="Description of the fix/resolution")
    partId: Optional[int] = Field(None, description="ID of the part used from inventory")
    quantityUsed: int = Field(default=0, ge=0, description="Quantity of the part used")
    laborHours: float = Field(default=2.0, gt=0, description="Total labor hours spent")
