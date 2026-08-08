import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, Float, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String, primary_key=True, default=gen_uuid)

    # 1. Origin & Customer Details
    complaint_source = Column(String(100))
    customer_name = Column(String(255))

    # 2. Product & Batch Identification
    product_name = Column(String(255))
    product_strength_grade = Column(String(100))
    batch_lot_number = Column(String(100))
    manufacturing_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    quantity_affected = Column(Float, nullable=True)
    quantity_unit = Column(String(20), default="kg")

    # 3. Complaint Details
    complaint_type = Column(String(100))
    complaint_date = Column(DateTime, nullable=True)
    detailed_description = Column(Text)

    # 4. Initial Assessment & Priority
    initial_severity = Column(
        Enum("Low", "Medium", "High", "Critical", name="severity_enum"),
        nullable=True,
    )
    priority = Column(
        Enum("Low", "Medium", "High", "Urgent", name="priority_enum"),
        nullable=True,
    )

    # AI metadata
    ai_extraction_confidence = Column(Float, nullable=True)
    ai_completeness_notes = Column(Text, nullable=True)

    status = Column(String(50), default="Pending Triage")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
