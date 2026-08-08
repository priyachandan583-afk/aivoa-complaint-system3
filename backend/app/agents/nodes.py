import json

from groq import Groq

from app.config import settings
from app.agents.prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    RISK_SYSTEM_PROMPT,
    COMPLETENESS_SYSTEM_PROMPT,
    CHAT_SYSTEM_PROMPT,
)

client = Groq(api_key=settings.groq_api_key)


def _call_groq(system_prompt: str, user_content: str, model: str) -> dict:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)


# --- LangGraph node functions ---
# Each node takes and returns the shared graph state dict.

def extract_fields_node(state: dict) -> dict:
    raw_text = state["raw_text"]
    fields = _call_groq(
        EXTRACTION_SYSTEM_PROMPT, raw_text, settings.groq_extraction_model
    )
    state["fields"] = fields
    return state


def completeness_check_node(state: dict) -> dict:
    fields_json = json.dumps(state["fields"])
    result = _call_groq(
        COMPLETENESS_SYSTEM_PROMPT, fields_json, settings.groq_extraction_model
    )
    state["missing_fields"] = result.get("missing_fields", [])
    state["completeness_notes"] = result.get("notes", "")
    return state


def risk_classification_node(state: dict) -> dict:
    fields_json = json.dumps(state["fields"])
    result = _call_groq(
        RISK_SYSTEM_PROMPT, fields_json, settings.groq_context_model
    )
    state["initial_severity"] = result.get("initial_severity")
    state["priority"] = result.get("priority")
    state["risk_notes"] = result.get("risk_notes")
    return state


def chat_response(question: str, complaint_context: dict) -> str:
    context_json = json.dumps(complaint_context)
    response = client.chat.completions.create(
        model=settings.groq_context_model,
        messages=[
            {"role": "system", "content": CHAT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Complaint record:\n{context_json}\n\nQuestion: {question}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
