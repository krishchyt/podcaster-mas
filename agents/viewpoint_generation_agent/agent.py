from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json
import os
import re # Import the regular expression module
from dotenv import load_dotenv

load_dotenv()

# Define the Viewpoint Generation Agent with a stricter instruction prompt
viewpoint_agent = Agent(
    name="viewpoint_generation_agent",
    model=LiteLlm(model="gemini/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    description="Generates two distinct and interesting viewpoints on a topic for a podcast conversation.",
    instruction=(
        "You are a JSON-only API. Your SOLE function is to generate two distinct viewpoints for a podcast topic. "
        "YOU MUST RESPOND WITH VALID JSON AND NOTHING ELSE. Do not include any introductory text, apologies, "
        "explanations, or markdown formatting. The output must be a raw JSON string. The JSON must be a list "
        "of two objects, where each object has 'host_name' and 'viewpoint' keys."
    )
)

session_service = InMemorySessionService()
runner = Runner(agent=viewpoint_agent, app_name="viewpoint_app", session_service=session_service)

USER_ID = "user_viewpoint"
SESSION_ID = "session_viewpoint"

async def execute(request: dict) -> dict:
    """Executes the viewpoint generation task with robust JSON parsing."""
    await session_service.create_session(app_name="viewpoint_app", user_id=USER_ID, session_id=SESSION_ID)
    
    prompt = (
        f"Generate two distinct viewpoints on the topic '{request['topic']}' "
        f"for hosts named {request['host_names'][0]} and {request['host_names'][1]}."
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print(f"--- Viewpoint Agent Raw Response ---\n{response_text}\n------------------------------------")

            # Use regex to find the JSON list within the response text
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            
            if not match:
                return {"error": "Viewpoint agent did not return a valid list structure."}
            
            json_string = match.group(0)
            try:
                viewpoints = json.loads(json_string)
                if isinstance(viewpoints, list) and len(viewpoints) == 2:
                    return {"viewpoints": viewpoints}
                else:
                    return {"error": "Viewpoint agent returned malformed data (not a list of 2)."}
            except json.JSONDecodeError:
                print(f"❌ Viewpoint Agent failed to parse JSON from extracted string: {json_string}")
                return {"error": "Viewpoint agent response contained invalid JSON."}
                
    return {"error": "No final response from viewpoint agent."}

