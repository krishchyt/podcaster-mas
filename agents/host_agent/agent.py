# agents/host_agent/agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv

load_dotenv()

host_agent = Agent(
    name="host_agent",
    model=LiteLlm(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    description="Orchestrates the podcast creation process.",
    instruction="You are the main coordinator."
)