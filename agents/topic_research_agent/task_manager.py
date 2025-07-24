# agents/topic_research_agent/task_manager.py
from .agent import execute

async def run(payload: dict) -> dict:
    """A simple wrapper to call the agent's execute function."""
    return await execute(payload)