from datetime import datetime
from typing import Tuple

from services.common.models import CanonicalGitHubEvent


class EnrichedGitHubEventV1(CanonicalGitHubEvent):
    # Time features
    event_date: str
    event_hour: int
    event_day_of_week: int
    is_weekend: bool

    # Repo features
    repo_owner: str
    repo_short_name: str

    # Actor features
    actor_login_normalized: str
    is_bot: bool

    # Normalized semantics
    activity_domain: str
    activity_action: str


EVENT_MAPPING: dict[str, Tuple[str, str]] = {
    "PushEvent": ("code_change", "push"),
    "PullRequestEvent": ("pr_mgmt", "pull_request"),
    "IssuesEvent": ("issue_mgmt", "issue"),
    "IssueCommentEvent": ("issue_mgmt", "comment"),
    "WatchEvent": ("collaboration", "watch"),
    "ForkEvent": ("collaboration", "fork"),
    "CreateEvent": ("repo_admin", "create"),
    "DeleteEvent": ("repo_admin", "delete"),
    "ReleaseEvent": ("repo_admin", "release"),
    "MemberEvent": ("collaboration", "member_change"),
    "PublicEvent": ("repo_admin", "made_public"),
}


def detect_bot(login: str) -> bool:
    login_lower = login.lower()

    if login_lower.endswith("[bot]"):
        return True

    if "bot" in login_lower and len(login_lower) > 6:
        return True

    return False


def enrich_event(event: CanonicalGitHubEvent) -> EnrichedGitHubEventV1:
    created = event.created_at

    # Time features
    event_date = created.date().isoformat()
    event_hour = created.hour
    event_day_of_week = created.weekday()
    is_weekend = event_day_of_week >= 5

    # Repo parsing
    if "/" in event.repo_name:
        repo_owner, repo_short_name = event.repo_name.split("/", 1)
    else:
        repo_owner = event.repo_name
        repo_short_name = event.repo_name

    # Actor features
    actor_login_normalized = event.actor_login.lower()
    is_bot = detect_bot(event.actor_login)

    # Event normalization
    domain, action = EVENT_MAPPING.get(event.event_type, ("other", "other"))

    return EnrichedGitHubEventV1(
        **event.model_dump(),

        event_date=event_date,
        event_hour=event_hour,
        event_day_of_week=event_day_of_week,
        is_weekend=is_weekend,

        repo_owner=repo_owner,
        repo_short_name=repo_short_name,

        actor_login_normalized=actor_login_normalized,
        is_bot=is_bot,

        activity_domain=domain,
        activity_action=action,
    )
