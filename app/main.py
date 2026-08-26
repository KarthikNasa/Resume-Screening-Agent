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

from app.services.embeddings import (
    similarity_percentage,
)

from app.services.scoring import (
    calculate_skill_score,
    calculate_final_score,
    get_recommendation,
)


app = FastAPI(
    title="AI Resume Screening Agent",
    version="3.0.0",
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


@app.get("/")
def home():

    return {
        "message": (
            "AI Resume Screening Agent "
            "is running"
        ),
        "version": "3.0.0",
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

    # -----------------------------------------
    # 1. Analyze the Job Description
    # -----------------------------------------

    required_skills = extract_skills(
        job_description
    )

    candidates = []

    errors = []

    successful = 0

    # -----------------------------------------
    # 2. Process Every Resume
    # -----------------------------------------

    for resume in resumes:

        filename = (
            resume.filename
            or "unknown"
        )

        extension = os.path.splitext(
            filename
        )[1].lower()

        # -------------------------------------
        # Check file type
        # -------------------------------------

        if extension not in [
            ".pdf",
            ".docx",
        ]:

            errors.append(
                f"{filename}: "
                "Unsupported file type"
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

            # ---------------------------------
            # Save temporary file
            # ---------------------------------

            with open(
                file_path,
                "wb",
            ) as buffer:

                shutil.copyfileobj(
                    resume.file,
                    buffer,
                )

            # ---------------------------------
            # Extract resume text
            # ---------------------------------

            resume_text = (
                extract_resume_text(
                    file_path
                )
            )

            if not resume_text.strip():

                errors.append(
                    f"{filename}: "
                    "No text found"
                )

                continue

            # ---------------------------------
            # Skill matching
            # ---------------------------------

            skill_result = (
                find_matching_skills(
                    resume_text,
                    required_skills,
                )
            )

            matched_skills = (
                skill_result[
                    "matched_skills"
                ]
            )

            missing_skills = (
                skill_result[
                    "missing_skills"
                ]
            )

            # ---------------------------------
            # Skill score
            # ---------------------------------

            skill_score = (
                calculate_skill_score(
                    matched_skills,
                    required_skills,
                )
            )

            # ---------------------------------
            # Semantic score
            # ---------------------------------

            semantic_score = (
                similarity_percentage(
                    job_description,
                    resume_text,
                )
            )

            # ---------------------------------
            # Final score
            # ---------------------------------

            final_score = (
                calculate_final_score(
                    skill_score,
                    semantic_score,
                )
            )

            recommendation = (
                get_recommendation(
                    final_score
                )
            )

            # ---------------------------------
            # Store candidate
            # ---------------------------------

            candidates.append(
                {
                    "filename": filename,

                    "score": final_score,

                    "skill_score": skill_score,

                    "semantic_score": (
                        semantic_score
                    ),

                    "matched_skills": (
                        matched_skills
                    ),

                    "missing_skills": (
                        missing_skills
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

            # ---------------------------------
            # Delete uploaded resume
            # ---------------------------------

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )

    # -----------------------------------------
    # 3. Rank Candidates
    # -----------------------------------------

    candidates.sort(
        key=lambda candidate:
        candidate["score"],
        reverse=True,
    )

    # -----------------------------------------
    # 4. Select Top 5
    # -----------------------------------------

    top_5 = candidates[:5]

    # -----------------------------------------
    # 5. Add Ranking
    # -----------------------------------------

    for index, candidate in enumerate(
        top_5,
        start=1,
    ):

        candidate["rank"] = index

    # -----------------------------------------
    # 6. Return Result
    # -----------------------------------------

    return {
        "total_resumes": len(resumes),

        "successful_resumes": successful,

        "failed_resumes": (
            len(resumes) - successful
        ),

        "required_skills": required_skills,

        "top_5": top_5,

        "errors": errors,
    }
