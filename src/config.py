import os
from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / ".env.prompt")


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "Banking Complaint App"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///bank_complaint.db"
    )
    # Synthetic banking users
    BANKING_ANALYST_ID = os.getenv("BANKING_ANALYST_ID","analyst_001")
    BANKING_ANALYST_TOKEN = os.getenv("BANKING_ANALYST_TOKEN")

    BANKING_SUPERVISOR_ID = os.getenv("BANKING_SUPERVISOR_ID","supervisor_001")
    BANKING_SUPERVISOR_TOKEN = os.getenv("BANKING_SUPERVISOR_TOKEN")

    BANKING_VIEWER_ID = os.getenv("BANKING_VIEWER_ID","viewer_001")
    BANKING_VIEWER_TOKEN = os.getenv("BANKING_VIEWER_TOKEN")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
    TRACE_FILE = Path(os.getenv("TRACE_FILE", "agent_traces.json"))
    PROMPT_AGENT = os.getenv("PROMPT_AGENT")

settings = Settings()
