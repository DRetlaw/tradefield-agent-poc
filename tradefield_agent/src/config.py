import os

MODEL = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-30b-a3b:free")
BASE_URL = "https://openrouter.ai/api/v1"
MAX_AGENT_STEPS = 8
