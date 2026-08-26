import os
import shutil
import uuid

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
)

from app.agents.jd_analyzer import (
    extract_skills,
)
from app.agents.resume_analyzer import (
    find_matching_skills,
)
from app.services.document_parser import (
    extract_resume_text,
)
from app.services.scoring import (
    calculate_skill_score,
    get_recommendation,
)


app = FastAPI(
    title="AI Resume Screening Agent",
    version="2.0.0",
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening Agent is running",
        "version": "2.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_resumes(
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...),
):

    required_skills = extract_skills(
        job_description
    )

    candidates = []

    errors = []

    successful = 0

    for resume in resumes:

        filename = resume.filename or "unknown"

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension not in [".pdf", ".docx"]:

            errors.append(
                f"{filename}: Unsupported file type"
            )

            continue

        unique_name = (
            f"{uuid.uuid4()}_{filename}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_name,
        )

        try:

            with open(
                file_path,
                "wb",
            ) as buffer:

                shutil.copyfileobj(
                    resume.file,
                    buffer,
                )

            resume_text = extract_resume_text(
                file_path
            )

            if not resume_text.strip():

                errors.append(
                    f"{filename}: No text found"
                )

                continue

            skill_result = find_matching_skills(
                resume_text,
                required_skills,
            )

            score = calculate_skill_score(
                skill_result[
                    "matched_skills"
                ],
                required_skills,
            )

            recommendation = get_recommendation(
                score
            )

            candidates.append(
                {
                    "filename": filename,
                    "score": score,
                    "matched_skills": (
                        skill_result[
                            "matched_skills"
                        ]
                    ),
                    "missing_skills": (
                        skill_result[
                            "missing_skills"
                        ]
                    ),
                    "recommendation": (
                        recommendation
                    ),
                }
            )

            successful += 1

        except Exception as exc:

            errors.append(
                f"{filename}: {str(exc)}"
            )

        finally:

            if os.path.exists(file_path):

                os.remove(file_path)

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    top_5 = candidates[:5]

    for index, candidate in enumerate(
        top_5,
        start=1,
    ):
        candidate["rank"] = index

    return {
        "total_resumes": len(resumes),
        "successful_resumes": successful,
        "failed_resumes": len(resumes)
        - successful,
        "required_skills": required_skills,
        "top_5": top_5,
        "errors": errors,
    }
