from typing import TypedDict


class SocialAgentState(TypedDict, total=False):
    topic: str
    platform: str

    research: list
    evaluation: str
    social_response: str

    quality_score: int
    approved: bool
    final_response: str

    retry_count: int