# AIVOA Customer Complaint Management System

AI-powered complaint intake for pharmaceutical (API/FDF) manufacturing, built for the
AIVOA Round 1 AI Product Engineer assignment.

## Architecture

```
Upload/Paste (React) → POST /complaints/extract (FastAPI)
    → file_parser.extract_text()  [PDF/DOCX/TXT/EML → raw text]
    → LangGraph pipeline (app/agents/graph.py):
         1. extract_fields_node   — Groq gemma2-9b-it, structured JSON extraction
         2. completeness_check_node — flags missing mandatory fields
         3. risk_classification_node — Groq llama-3.3-70b-versatile, severity/priority
    → JSON returned to frontend → Redux populates Log Customer Complaint form
    → user reviews/edits → POST /complaints → saved to Postgres/MySQL
```

Chat copilot: `POST /complaints/chat` sends the saved complaint record as context to a
Groq model and returns a grounded answer.

## Setup

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY and DATABASE_URL
uvicorn app.main:app --reload
```
Runs on `http://localhost:8000`. Swagger docs at `/docs`.

### Database
Create the DB first (Postgres example):
```bash
createdb aivoa_complaints
```
Tables are auto-created on first run via `Base.metadata.create_all`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on `http://localhost:5173`, proxies `/api/*` to the backend.

## What's implemented

- Two-panel UI matching the reference screenshot: complaint form (left) + AI intake
  assistant (right, upload/paste + chat).
- Redux Toolkit slices for form fields and assistant/chat state.
- FastAPI backend with full CRUD for complaints.
- LangGraph 3-node pipeline: extraction → completeness check → risk classification.
- Groq LLM calls using `gemma2-9b-it` for extraction/completeness and
  `llama-3.3-70b-versatile` for risk classification and chat, as specified.
- Bonus features included: **Complaint Completeness Checker** and **AI Risk
  Classification** (severity/priority auto-filled with rationale).

## What you still need to do before submitting

1. Add your real `GROQ_API_KEY` and test extraction against a few sample complaint
   documents you write yourself (the assignment explicitly allows this).
2. Wire up whichever additional bonus features you want (duplicate detection and CAPA
   recommendation are the two not yet built — see "Extending" below).
3. Record the two demo videos: (a) product walkthrough, (b) code walkthrough from
   frontend upload → API → LangGraph → DB → form population.
4. Push to GitHub and fill out the submission form.

## Extending with more bonus features

- **Duplicate Complaint Detection**: add a node that embeds `detailed_description`
  (e.g. via a Groq/embedding call or simple TF-IDF) and compares against existing
  complaints fetched from `GET /complaints`.
- **CAPA Recommendation**: add a `capa_recommendation_node` after risk classification
  with its own prompt in `prompts.py`, store the result in a new `capa_notes` column.
- **Complaint Summary**: reuse `detailed_description` from extraction — already
  produced as a concise LLM summary rather than raw pasted text.

## Notes

- Production-grade OCR is not implemented (not required) — `file_parser.py` handles
  text-based PDF/DOCX/TXT/EML only.
- All LLM calls request `response_format: json_object` from Groq to keep parsing
  reliable; no manual markdown-fence stripping needed as a result.
