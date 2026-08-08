from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from app.agents.nodes import (
    extract_fields_node,
    completeness_check_node,
    risk_classification_node,
)


class ComplaintExtractionState(TypedDict, total=False):
    raw_text: str
    fields: dict
    missing_fields: list
    completeness_notes: str
    initial_severity: Optional[str]
    priority: Optional[str]
    risk_notes: Optional[str]


def build_extraction_graph():
    graph = StateGraph(ComplaintExtractionState)

    graph.add_node("extract_fields", extract_fields_node)
    graph.add_node("check_completeness", completeness_check_node)
    graph.add_node("classify_risk", risk_classification_node)

    graph.set_entry_point("extract_fields")
    graph.add_edge("extract_fields", "check_completeness")
    graph.add_edge("check_completeness", "classify_risk")
    graph.add_edge("classify_risk", END)

    return graph.compile()


# Compiled once at import time; reused across requests.
extraction_graph = build_extraction_graph()


def run_extraction_pipeline(raw_text: str) -> ComplaintExtractionState:
    """Entry point called by the FastAPI route."""
    result = extraction_graph.invoke({"raw_text": raw_text})
    return result
