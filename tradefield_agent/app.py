import os
import gradio as gr
from dotenv import load_dotenv
from src.agent import TradeFieldAgent

load_dotenv()

agent = None

def get_agent():
    global agent
    if agent is None:
        agent = TradeFieldAgent()
    return agent

def run_agent(request, approve):
    if not request.strip():
        return "Please enter a customer/job request.", "{}"
    try:
        result = get_agent().run(request, approved=approve)
        return result["response"], result
    except Exception as exc:
        return f"Error: {exc}", {"error": str(exc)}

with gr.Blocks(title="TradeField Agent") as demo:
    gr.Markdown("# 🔧 TradeField Agent\nAgentic AI POC for field-service lead handling.")
    request = gr.Textbox(
        label="Customer / job request",
        lines=6,
        value="Customer says the kitchen mixer tap is leaking and wants it replaced tomorrow."
    )
    approve = gr.Checkbox(
        label="Human approval for simulated job-board write",
        value=False
    )
    run = gr.Button("Run Agent")
    answer = gr.Markdown(label="Agent response")
    trace = gr.JSON(label="Agent trace")
    run.click(run_agent, inputs=[request, approve], outputs=[answer, trace])

demo.launch()
