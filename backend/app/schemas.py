from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ComplaintBase(BaseModel):
    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    product_strength_grade: Optional[str] = None
    batch_lot_number: Optional[str] = None
    manufacturing_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    quantity_affected: Optional[float] = None
    quantity_unit: Optional[str] = "kg"
    complaint_type: Optional[str] = None
    complaint_date: Optional[datetime] = None
    detailed_description: Optional[str] = None
    initial_severity: Optional[str] = None
    priority: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(ComplaintBase):
    pass


class ComplaintOut(ComplaintBase):
    id: str
    status: str
    ai_extraction_confidence: Optional[float] = None
    ai_completeness_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExtractionResult(BaseModel):
    """What the LangGraph pipeline returns to populate the form."""
    fields: ComplaintBase
    confidence: float
    missing_fields: list[str] = []
    risk_notes: Optional[str] = None


class ChatMessage(BaseModel):
    message: str
    complaint_id: Optional[str] = None
