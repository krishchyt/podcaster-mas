from common.a2a_client import call_agent

# Define the URLs for the specialized agents
TOPIC_RESEARCH_URL = "http://localhost:8001/run"
VIEWPOINT_GENERATION_URL = "http://localhost:8002/run"
SCRIPTWRITING_URL = "http://localhost:8003/run"

async def run(payload: dict) -> dict:
    """
    Orchestrates the podcast creation process with enhanced logging and error handling.
    """
    print("--- 🚀 HOST AGENT: Orchestration Started ---")
    print(f"Initial Payload: {payload}")

    # 1. Call Topic Research Agent
    print("\n[1/3] 🔍 Calling Topic Research Agent...")
    research_result = await call_agent(TOPIC_RESEARCH_URL, {"topic": payload["topic"]})
    if "error" in research_result:
        print(f"❌ ERROR from Topic Research Agent: {research_result['error']}")
        return research_result
    print("✅ Research received.")
    print(f"   -> Research Data (truncated): {research_result.get('research', '')[:100]}...")


    # 2. Call Viewpoint Generation Agent
    print("\n[2/3] 🤔 Calling Viewpoint Generation Agent...")
    viewpoints_result = await call_agent(VIEWPOINT_GENERATION_URL, payload)
    if "error" in viewpoints_result:
        print(f"❌ ERROR from Viewpoint Generation Agent: {viewpoints_result['error']}")
        return viewpoints_result
    print("✅ Viewpoints received.")
    print(f"   -> Viewpoint Data: {viewpoints_result.get('viewpoints', [])}")


    # 3. Call Scriptwriting Agent
    print("\n[3/3] ✍️ Calling Scriptwriting Agent...")
    scriptwriting_payload = {
        "topic": payload["topic"],
        "host_names": payload["host_names"],
        "tone": payload["tone"],
        "research": research_result.get("research", ""),
        "viewpoints": viewpoints_result.get("viewpoints", [])
    }
    final_script = await call_agent(SCRIPTWRITING_URL, scriptwriting_payload)
    if "error" in final_script:
        print(f"❌ ERROR from Scriptwriting Agent: {final_script['error']}")
        return final_script
    
    print("\n🎉 --- HOST AGENT: Orchestration Complete ---")
    return final_script
