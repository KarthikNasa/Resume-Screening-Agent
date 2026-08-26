from pydantic import BaseModel
from typing import List


class CandidateResult(BaseModel):
    rank: int
    filename: str

    score: float

    skill_score: float
    semantic_score: float

    matched_skills: List[str]
    missing_skills: List[str]

    recommendation: str


class AnalysisResponse(BaseModel):
    total_resumes: int
    successful_resumes: int
    failed_resumes: int

    required_skills: List[str]

    top_5: List[CandidateResult]

    errors: List[str]
