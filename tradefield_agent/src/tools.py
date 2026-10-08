from datetime import datetime, timedelta
from typing import Any, Dict, List
import uuid

PARTS = {
    "mixer tap": {"sku": "TAP-MIX-001", "name": "Standard mixer tap", "price": 89.0},
    "isolation valve": {"sku": "VAL-ISO-001", "name": "15mm isolation valve", "price": 12.0},
    "led downlight": {"sku": "LED-DL-001", "name": "LED downlight", "price": 18.0},
    "power outlet": {"sku": "ELEC-PO-001", "name": "Standard power outlet", "price": 14.0},
}

STANDARD_JOBS = {
    "tap replacement": {"labour": 120.0, "materials": 101.0},
    "tap repair": {"labour": 90.0, "materials": 25.0},
    "light fitting replacement": {"labour": 110.0, "materials": 45.0},
}

def check_safety(job_description: str) -> Dict[str, Any]:
    text = job_description.lower()
    danger_terms = [
        "sparks", "switchboard", "burning smell", "gas leak",
        "exposed wire", "live wire", "smoke", "fire", "electrocution"
    ]
    hits = [x for x in danger_terms if x in text]
    if hits:
        return {
            "status": "ESCALATE",
            "severity": "HIGH",
            "matched_indicators": hits,
            "message": "Safety-sensitive indicators detected. Do not provide work instructions. Escalate to a qualified professional/emergency service as appropriate."
        }
    return {
        "status": "CLEAR_FOR_ADMIN_WORKFLOW",
        "severity": "LOW",
        "matched_indicators": [],
        "message": "No high-risk indicators detected by this simple POC rule set."
    }

def extract_job_info(customer_message: str) -> Dict[str, Any]:
    return {
        "job_id": f"JOB-{uuid.uuid4().hex[:8].upper()}",
        "raw_request": customer_message,
        "source": "demo",
        "status": "INTAKE_COMPLETE"
    }

def estimate_quote(job_type: str, urgency: str = "standard") -> Dict[str, Any]:
    key = job_type.lower().strip()
    if key not in STANDARD_JOBS:
        return {
            "status": "NO_STANDARD_QUOTE",
            "reason": "Job type is not in the demo catalogue.",
            "quote": None
        }
    base = STANDARD_JOBS[key]
    multiplier = 1.25 if urgency.lower() == "urgent" else 1.0
    subtotal = (base["labour"] + base["materials"]) * multiplier
    return {
        "status": "ESTIMATE_ONLY",
        "currency": "AUD",
        "job_type": job_type,
        "urgency": urgency,
        "labour": round(base["labour"] * multiplier, 2),
        "materials": round(base["materials"] * multiplier, 2),
        "estimated_total": round(subtotal, 2),
        "disclaimer": "Non-binding estimate for demonstration only."
    }

def lookup_part(part_query: str) -> Dict[str, Any]:
    q = part_query.lower()
    matches = []
    for key, value in PARTS.items():
        if q in key or key in q:
            matches.append(value)
    return {"query": part_query, "matches": matches, "count": len(matches)}

def propose_appointment(preferred_day: str = "next business day") -> Dict[str, Any]:
    # Simulation only: no calendar is changed.
    return {
        "status": "PROPOSED_NOT_BOOKED",
        "preferred_day": preferred_day,
        "options": [
            "09:00-10:00",
            "11:00-12:00",
            "14:00-15:00"
        ],
        "requires_human_approval": True
    }

def create_job_record(job: Dict[str, Any], approved: bool = False) -> Dict[str, Any]:
    if not approved:
        return {
            "status": "BLOCKED",
            "reason": "Human approval required before external write."
        }
    return {
        "status": "SIMULATED_CREATED",
        "external_system": "DEMO_JOB_BOARD",
        "external_id": f"DEMO-{uuid.uuid4().hex[:10].upper()}",
        "payload": job
    }

def list_tool_schemas() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "check_safety",
                "description": "Check whether the customer request contains obvious high-risk indicators. Use before quoting or scheduling.",
                "parameters": {
                    "type": "object",
                    "properties": {"job_description": {"type": "string"}},
                    "required": ["job_description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "extract_job_info",
                "description": "Create a structured demo job intake record from the customer's request.",
                "parameters": {
                    "type": "object",
                    "properties": {"customer_message": {"type": "string"}},
                    "required": ["customer_message"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "estimate_quote",
                "description": "Create a non-binding estimate for one of the demo standard job types.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_type": {"type": "string"},
                        "urgency": {"type": "string"}
                    },
                    "required": ["job_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "lookup_part",
                "description": "Look up a part in the small demo parts catalogue.",
                "parameters": {
                    "type": "object",
                    "properties": {"part_query": {"type": "string"}},
                    "required": ["part_query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "propose_appointment",
                "description": "Propose appointment slots. This does not book anything.",
                "parameters": {
                    "type": "object",
                    "properties": {"preferred_day": {"type": "string"}},
                    "required": []
                }
            }
        }
    ]

TOOL_IMPL = {
    "check_safety": check_safety,
    "extract_job_info": extract_job_info,
    "estimate_quote": estimate_quote,
    "lookup_part": lookup_part,
    "propose_appointment": propose_appointment,
}
