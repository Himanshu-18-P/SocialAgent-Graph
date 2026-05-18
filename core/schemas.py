from pydantic import BaseModel
from typing import List


class QualityCheckResponse(BaseModel):
    score: int
    approved: bool
    issues: List[str]
    improved_response: str