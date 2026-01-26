from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class CanonicalGitHubEvent(BaseModel):
    # Event
    event_id: str
    event_type: str
    created_at: datetime
    is_public: bool

    # Actor
    actor_id: int
    actor_login: str
    actor_display_login: str

    # Repo
    repo_id: int
    repo_name: str

    # Org (optional)
    org_id: Optional[int]
    org_login: Optional[str]

    # Payload (kept raw for now)
    payload: Dict[str, Any]
