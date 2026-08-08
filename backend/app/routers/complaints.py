from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Complaint
from app.schemas import ComplaintCreate, ComplaintOut, ChatMessage
from app.services.file_parser import extract_text
from app.agents.graph import run_extraction_pipeline
from app.agents.nodes import chat_response

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post("/extract")
async def extract_complaint(
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
):
    """
    Accepts either an uploaded document OR pasted text, runs the LangGraph
    extraction pipeline, and returns structured fields to populate the form.
    """
    if file:
        file_bytes = await file.read()
        raw_text = extract_text(file.filename, file_bytes)
    elif text:
        raw_text = text
    else:
        raise HTTPException(400, "Provide either a file or text")

    if not raw_text.strip():
        raise HTTPException(422, "Could not extract any text from the input")

    result = run_extraction_pipeline(raw_text)

    return {
        "fields": result.get("fields", {}),
        "missing_fields": result.get("missing_fields", []),
        "completeness_notes": result.get("completeness_notes"),
        "initial_severity": result.get("initial_severity"),
        "priority": result.get("priority"),
        "risk_notes": result.get("risk_notes"),
    }


@router.post("", response_model=ComplaintOut)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db)):
    complaint = Complaint(**payload.model_dump())
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.get("", response_model=list[ComplaintOut])
def list_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()


@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintOut)
def update_complaint(complaint_id: str, payload: ComplaintCreate, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(complaint, k, v)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: str, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    db.delete(complaint)
    db.commit()
    return {"ok": True}


@router.post("/chat")
def chat(payload: ChatMessage, db: Session = Depends(get_db)):
    context = {}
    if payload.complaint_id:
        complaint = db.query(Complaint).filter(Complaint.id == payload.complaint_id).first()
        if complaint:
            context = {c.name: getattr(complaint, c.name) for c in complaint.__table__.columns}
    reply = chat_response(payload.message, context)
    return {"reply": reply}
