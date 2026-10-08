import json
import os
from typing import Any, Dict, List
from openai import OpenAI
from .config import BASE_URL, MODEL, MAX_AGENT_STEPS
from .tools import list_tool_schemas, TOOL_IMPL, create_job_record

SYSTEM_PROMPT = """You are TradeField Agent, an educational field-operations assistant.

Goal:
Help busy tradespeople avoid losing customer leads and reduce administrative work.

You may:
- understand customer requests
- check obvious safety indicators
- create structured intake
- create non-binding standard-job estimates
- look up demo parts
- propose appointment slots
- prepare a simulated job-board payload

Rules:
1. Call check_safety before quoting or scheduling.
2. If safety returns ESCALATE, do not give technical repair instructions. Explain that the case needs qualified human handling.
3. Never claim an appointment is booked. The appointment tool only proposes slots.
4. Never claim a quote is final. Estimates are non-binding.
5. Never invent catalogue facts.
6. Before any external write, require human approval.
7. If information is missing, ask for it instead of inventing it.
8. Keep field-worker output concise.
"""

class TradeFieldAgent:
    def __init__(self, api_key: str | None = None, model: str = MODEL):
        key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not key:
            raise ValueError("OPENROUTER_API_KEY is required")
        self.client = OpenAI(base_url=BASE_URL, api_key=key)
        self.model = model

    def _chat(self, messages: List[Dict[str, Any]]):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=list_tool_schemas(),
            tool_choice="auto",
            temperature=0.1,
        )

    def run(self, user_request: str, approved: bool = False) -> Dict[str, Any]:
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ]
        trace = []

        for step in range(MAX_AGENT_STEPS):
            response = self._chat(messages)
            msg = response.choices[0].message

            if msg.tool_calls:
                messages.append(msg.model_dump(exclude_none=True))
                for call in msg.tool_calls:
                    name = call.function.name
                    args = json.loads(call.function.arguments or "{}")
                    trace.append({"step": step + 1, "tool": name, "args": args})

                    fn = TOOL_IMPL.get(name)
                    if not fn:
                        result = {"error": f"Unknown tool: {name}"}
                    else:
                        try:
                            result = fn(**args)
                        except Exception as exc:
                            result = {"error": str(exc)}

                    if name == "check_safety" and result.get("status") == "ESCALATE":
                        # Give the model the safety result and let it formulate the user-facing escalation.
                        pass

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result),
                    })
                continue

            final_text = msg.content or ""
            result = {
                "status": "COMPLETED",
                "response": final_text,
                "trace": trace,
                "steps": len(trace),
                "approval_required": True,
                "approved": approved,
            }

            if approved:
                job_payload = {
                    "customer_request": user_request,
                    "agent_response": final_text,
                    "trace": trace,
                }
                result["write_result"] = create_job_record(job_payload, approved=True)
            else:
                result["write_result"] = create_job_record({}, approved=False)

            return result

        return {
            "status": "MAX_STEPS_REACHED",
            "response": "The agent reached its tool-call limit. Please review the request manually.",
            "trace": trace,
            "steps": len(trace),
        }
