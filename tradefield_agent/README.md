# TradeField Agent — Agentic AI Field Operations POC

A hands-on Agentic AI project inspired by the problem behind BackOnTools: tradies lose leads and time because they are busy on-site and cannot answer calls, qualify work, prepare safe next steps, or keep job-management systems updated.

## What this POC builds

A **TradeField Agent** that receives a customer/job request and autonomously:

1. Understands the job request.
2. Checks for safety-sensitive situations.
3. Extracts structured customer/job information.
4. Estimates a **non-binding** ballpark quote for standard jobs.
5. Looks up parts/material information from a small local catalogue.
6. Proposes an appointment slot.
7. Produces a job-management payload.
8. Stops for human approval before any consequential action.
9. Returns a concise field-worker summary.

The POC uses **OpenRouter** for the LLM and deliberately simulates external business systems.

## Agentic concepts covered

- Tool/function calling
- ReAct-style control loop
- State and memory
- Tool registry
- Safety guardrails
- Human-in-the-loop approval
- Structured outputs
- Deterministic business tools
- Observability / traces
- Evaluation test cases
- Gradio UI
- API-ready architecture

## Safety boundary

This is an educational prototype, not a trade-compliance or engineering system. It must not be used to authorize electrical, gas, structural, plumbing, or other regulated work. Safety-sensitive jobs are escalated to a qualified human.

No real customer records, bookings, payments, SMS messages, ServiceM8 records, or field-control actions are performed.

## Current model

The notebook defaults to:

`qwen/qwen3-30b-a3b:free`

OpenRouter currently lists this model as free and confirms support for tool calling and structured outputs. See:
https://openrouter.ai/qwen/qwen3-30b-a3b:free

## Run in Google Colab

Open:

`notebooks/tradefield_agent_colab.ipynb`

Then run the cells from top to bottom.

You need an OpenRouter API key. Put it into Colab Secrets as:

`OPENROUTER_API_KEY`

Do not commit the key.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Then open the Gradio URL.

## Git

```bash
git init
git add .
git commit -m "Build TradeField agent POC"
git branch -M main
git remote add origin https://github.com/YOUR_USER/tradefield-agent.git
git push -u origin main
```

## Suggested learning progression

### Exercise 1 — Direct LLM
Ask the model to turn a customer message into structured job information.

### Exercise 2 — First tool
Add `check_safety`.

### Exercise 3 — Tool-calling agent
Allow the model to decide which tools to call.

### Exercise 4 — Multi-tool workflow
Use safety, quote, parts and scheduling tools.

### Exercise 5 — State
Persist a job state dictionary through the whole run.

### Exercise 6 — Human approval
Block booking / external write operations until a human approves.

### Exercise 7 — Business integration
Replace the simulated job-board tool with a real connector later.

### Exercise 8 — Evaluation
Run the included adversarial test cases and measure:
- correct escalation
- correct tool choice
- quote correctness
- missing-information detection
- no unsafe action

### Exercise 9 — Deployment
Deploy the API/UI using a free personal-development hosting tier where available, while keeping the OpenRouter key server-side.

## Example scenarios

Safe:
> "Customer wants a leaking tap replaced. Kitchen tap, standard mixer, access is easy."

Needs clarification:
> "Need a new hot water system."

Safety escalation:
> "There are sparks coming from the switchboard and the lights keep flickering."

The agent should not provide instructions for working on the switchboard. It should escalate.

## Architecture

```text
Customer / Field Worker
        |
        v
  TradeField Agent
        |
        +---- OpenRouter LLM
        |
        +---- Safety Tool
        +---- Job Intake Tool
        +---- Quote Tool
        +---- Parts Catalogue
        +---- Appointment Tool
        +---- Job-board Adapter
        |
        v
 Human Approval Gate
        |
        v
 Simulated Job Record
```
