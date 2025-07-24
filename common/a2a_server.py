# common/a2a_server.py
from fastapi import FastAPI

def create_app(agent):
    """
    Creates a standard FastAPI application for an agent.
    """
    app = FastAPI()

    @app.post("/run")
    async def run(payload: dict):
        return await agent.execute(payload)

    return app