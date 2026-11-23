import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient

from src.config import settings

MODEL = settings.OLLAMA_MODEL
TRACE_FILE = settings.TRACE_FILE
SYSTEM_PROMPT = settings.PROMPT_AGENT

async def investigate(question: str) -> str:

    mcp_client = MultiServerMCPClient({
        "banking": {
            "transport": "stdio",
            "command": sys.executable,
            "args": ["-m", "src.mcp.mcp_server"],
        }
    })

    # Retrieve MCP tools as LangChain tools
    tools = await mcp_client.get_tools()

    if not tools:
        raise RuntimeError("No investigation tools available.")

    # Local LLM
    model = ChatOllama(model=MODEL,temperature=0)

    # Build LangChain agent
    agent = create_agent(model=model,tools=tools,system_prompt=SYSTEM_PROMPT)

    # Record tool execution traces
    
    traces = []

    try:
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]},
            config={"recursion_limit": 12},
        )

        for message in result["messages"]:
            if message.type == "tool":

                status = getattr(message, "status", None)
                if status not in {"success", "error"}:
                    status = "unknown"

                traces.append({
                    "timestamp": datetime.now(
                        timezone.utc
                    ).isoformat(),
                    "tool": message.name,
                    "status": status,
                })

        return result["messages"][-1].content

    except Exception as error:
        traces.append({
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "event": "investigation_failed",
            "status": "error",
            "error_type": type(error).__name__,
        })

        raise

    finally:
        TRACE_FILE.write_text(
            json.dumps(traces, indent=2),
            encoding="utf-8"
        )