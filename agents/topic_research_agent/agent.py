# agents/topic_research_agent/agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

topic_research_agent = Agent(
    name="topic_research_agent",
    model=LiteLlm(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    description="Researches a given topic.",
    instruction="You are a research assistant. Given a topic, find relevant facts, statistics, and recent developments. Present the information as a concise summary."
)

session_service = InMemorySessionService()
runner = Runner(
    agent=topic_research_agent,
    app_name="topic_research_app",
    session_service=session_service
)

USER_ID = "user_research"
SESSION_ID = "session_research"

async def execute(request: dict) -> dict:
    """Executes the research task."""
    await session_service.create_session(
        app_name="topic_research_app", user_id=USER_ID, session_id=SESSION_ID
    )
    prompt = f"Please research the following topic: {request['topic']}"
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"research": event.content.parts[0].text}
    return {"research": "No response generated."}