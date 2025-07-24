# agents/scriptwriting_agent/agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

scriptwriting_agent = Agent(
    name="scriptwriting_agent",
    model=LiteLlm(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    description="Writes a conversational podcast script.",
    instruction="You are a professional podcast scriptwriter. Write an engaging script between two hosts. Use the provided research and viewpoints to shape the dialogue. The script should have an introduction, main discussion, and a conclusion. Match the requested tone."
)

session_service = InMemorySessionService()
runner = Runner(
    agent=scriptwriting_agent,
    app_name="scriptwriting_app",
    session_service=session_service
)

USER_ID = "user_scriptwriter"
SESSION_ID = "session_scriptwriter"

async def execute(request: dict) -> dict:
    """Executes the scriptwriting task."""
    await session_service.create_session(
        app_name="scriptwriting_app", user_id=USER_ID, session_id=SESSION_ID
    )
    host1, host2 = request['host_names'][0], request['host_names'][1]
    viewpoint1 = next((vp['viewpoint'] for vp in request['viewpoints'] if vp['host_name'] == host1), "")
    viewpoint2 = next((vp['viewpoint'] for vp in request['viewpoints'] if vp['host_name'] == host2), "")

    prompt = (
        f"Write a podcast script on the topic '{request['topic']}'.\n"
        f"The hosts are {host1} and {host2}.\n"
        f"The tone is: {request['tone']}.\n\n"
        f"Host {host1}'s viewpoint: {viewpoint1}\n"
        f"Host {host2}'s viewpoint: {viewpoint2}\n\n"
        f"Incorporate this research:\n{request['research']}\n\n"
        "Include a title for the episode."
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            title = "Untitled Podcast"
            if "Title:" in response_text:
                parts = response_text.split("Title:", 1)[1].split("\n", 1)
                title = parts[0].strip()
                script = parts[1].strip() if len(parts) > 1 else ""
            else:
                script = response_text
            return {"title": title, "script": script}
            
    return {"title": "Error", "script": "Failed to generate script."}