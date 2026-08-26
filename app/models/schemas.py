from pydantic import BaseModel
from typing import List


class CandidateResult(BaseModel):

    rank: int

    filename: str

    score: float

    skill_score: float

    semantic_score: float

    experience_score: float

    preferred_score: float

    education_score: float

    certification_score: float

    candidate_experience_years: float

    required_experience_years: float

    matched_skills: List[str]

    missing_skills: List[str]

    preferred_skills: List[str]

    education: List[str]

    missing_mandatory: List[str]

    recommendation: str


class AnalysisResponse(BaseModel):

    total_resumes: int

    successful_resumes: int

    failed_resumes: int

    required_skills: List[str]

    preferred_skills: List[str]

    required_experience_years: float

    top_5: List[CandidateResult]

    errors: List[str]
