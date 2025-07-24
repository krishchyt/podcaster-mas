from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the Host Agent
host_agent = Agent(
    name="host_agent",
    model=LiteLlm(
        model="gemini/gemini-pro",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    description="Orchestrates the podcast creation process by coordinating with specialized agents.",
    instruction="You are the main coordinator. Your role is to manage the podcast creation workflow."
)

# Initialize session service and runner for the agent
session_service = InMemorySessionService()
runner = Runner(
    agent=host_agent,
    app_name="host_app",
    session_service=session_service
)

# Dummy execute function as orchestration is handled in task_manager.py
async def execute(request: dict) -> dict:
    """This function is a placeholder as the main logic is in the task manager."""
    return {"status": "Payload passed to task manager for orchestration."}