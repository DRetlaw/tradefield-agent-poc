from src.tools import check_safety, estimate_quote, lookup_part, propose_appointment

def test_safety_escalation():
    r = check_safety("There are sparks from the switchboard.")
    assert r["status"] == "ESCALATE"

def test_safe_admin_request():
    r = check_safety("Replace a leaking kitchen mixer tap.")
    assert r["status"] == "CLEAR_FOR_ADMIN_WORKFLOW"

def test_quote():
    r = estimate_quote("tap replacement")
    assert r["status"] == "ESTIMATE_ONLY"
    assert r["estimated_total"] > 0

def test_part():
    r = lookup_part("mixer tap")
    assert r["count"] == 1

def test_appointment_is_not_booking():
    r = propose_appointment()
    assert r["status"] == "PROPOSED_NOT_BOOKED"
