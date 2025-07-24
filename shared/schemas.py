from pydantic import BaseModel
from typing import List

class PodcastRequest(BaseModel):
    """Defines the user's request for a new podcast episode."""
    topic: str
    host_names: List[str]
    tone: str

class PodcastScript(BaseModel):
    """Defines the final generated podcast script."""
    title: str
    script: str