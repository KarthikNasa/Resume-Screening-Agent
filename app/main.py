from fastapi import FastAPI

from app.agents.jd_analyzer import extract_skills
from app.agents.resume_analyzer import find_matching_skills
from app.agents.ranking_agent import rank_candidates


app = FastAPI(
    title="AI Resume Screening Agent",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/test-ranking")
def test_ranking(data: dict):

    job_description = data.get(
        "job_description",
        "",
    )

    resumes = data.get(
        "resumes",
        [],
    )

    required_skills = extract_skills(
        job_description
    )

    candidates = []

    for resume in resumes:

        resume_name = resume.get(
            "name",
            "Unknown",
        )

        resume_text = resume.get(
            "text",
            "",
        )

        skill_result = find_matching_skills(
            resume_text,
            required_skills,
        )

        candidates.append(
            {
                "name": resume_name,
                **skill_result,
            }
        )

    ranked = rank_candidates(
        candidates,
        required_skills,
    )

    return {
        "required_skills": required_skills,
        "total_candidates": len(ranked),
        "top_5": ranked[:5],
    }

