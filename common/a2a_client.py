# common/a2a_client.py
import httpx

async def call_agent(url: str, payload: dict) -> dict:
    """
    An asynchronous client to send requests to other agents via the A2A protocol.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return {"error": f"Failed to communicate with agent at {url}."}