import os
import shutil
import uuid

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# =========================================
# AGENTS
# =========================================

from app.agents.jd_analyzer import (
    extract_skills,
    extract_experience_years,
    extract_education,
)

from app.agents.resume_analyzer import (
    find_matching_skills,
)

from app.agents.requirements_analyzer import (
    extract_required_skills,
    extract_preferred_skills,
    extract_minimum_experience,
)


# =========================================
# SERVICES
# =========================================

from app.services.document_parser import (
    extract_resume_text,
)

from app.services.embeddings import (
    similarity_percentage,
)

from app.services.scoring import (
    calculate_skill_score,
    calculate_experience_score,
    calculate_preferred_score,
    calculate_education_score,
    calculate_certification_score,
    calculate_final_score,
    get_recommendation,
)

from app.services.mandatory_check import (
    check_mandatory_skills,
    apply_mandatory_penalty,
)


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="AI Resume Screening Agent",
    version="4.0.0",
)


# =========================================
# DIRECTORIES
# =========================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


# =========================================
# FRONTEND
# =========================================

app.mount(
    "/static",
    StaticFiles(
        directory="frontend"
    ),
    name="static",
)


# =========================================
# HOME PAGE
# =========================================

@app.get("/")
def home():

    return FileResponse(
        "frontend/index.html"
    )


# =========================================
# FRONTEND ALTERNATIVE URL
# =========================================

@app.get("/app")
def frontend():

    return FileResponse(
        "frontend/index.html"
    )


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================
# RESUME ANALYSIS
# =========================================

@app.post("/analyze")
async def analyze_resumes(

    job_description: str = Form(...),

    resumes: list[UploadFile] = File(...),

):

    # =====================================
    # ANALYZE JOB DESCRIPTION
    # =====================================

    required_skills = (
        extract_required_skills(
            job_description
        )
    )

    preferred_skills = (
        extract_preferred_skills(
            job_description
        )
    )

    required_experience = (
        extract_minimum_experience(
            job_description
        )
    )


    # =====================================
    # RESULT STORAGE
    # =====================================

    candidates = []

    errors = []

    successful = 0


    # =====================================
    # PROCESS EACH RESUME
    # =====================================

    for resume in resumes:

        filename = (
            resume.filename
            or "unknown"
        )

        extension = os.path.splitext(
            filename
        )[1].lower()


        # ---------------------------------
        # CHECK FILE TYPE
        # ---------------------------------

        if extension not in [
            ".pdf",
            ".docx",
        ]:

            errors.append(
                f"{filename}: "
                "Unsupported file type"
            )

            continue


        # ---------------------------------
        # CREATE TEMP FILE
        # ---------------------------------

        unique_name = (
            f"{uuid.uuid4()}_{filename}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_name
        )


        try:

            # =============================
            # SAVE FILE
            # =============================

            with open(
                file_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    resume.file,
                    buffer
                )


            # =============================
            # EXTRACT RESUME TEXT
            # =============================

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


            # =============================
            # RESUME INFORMATION
            # =============================

            candidate_skills = (
                extract_skills(
                    resume_text
                )
            )


            candidate_experience = (
                extract_experience_years(
                    resume_text
                )
            )


            education = (
                extract_education(
                    resume_text
                )
            )


            # =============================
            # MATCH REQUIRED SKILLS
            # =============================

            skill_result = (
                find_matching_skills(
                    resume_text,
                    required_skills
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


            # =============================
            # SKILL SCORE
            # =============================

            skill_score = (
                calculate_skill_score(
                    matched_skills,
                    required_skills
                )
            )


            # =============================
            # PREFERRED SKILLS
            # =============================

            preferred_score = (
                calculate_preferred_score(
                    candidate_skills,
                    preferred_skills
                )
            )


            # =============================
            # EXPERIENCE
            # =============================

            experience_score = (
                calculate_experience_score(
                    candidate_experience,
                    required_experience
                )
            )


            # =============================
            # EDUCATION
            # =============================

            education_score = (
                calculate_education_score(
                    education
                )
            )


            # =============================
            # CERTIFICATION
            # =============================

            certification_score = (
                calculate_certification_score(
                    resume_text
                )
            )


            # =============================
            # SEMANTIC SIMILARITY
            # =============================

            semantic_score = (
                similarity_percentage(
                    job_description,
                    resume_text
                )
            )


            # =============================
            # FINAL SCORE
            # =============================

            final_score = (
                calculate_final_score(

                    skill_score=skill_score,

                    semantic_score=semantic_score,

                    experience_score=experience_score,

                    preferred_score=preferred_score,

                    education_score=education_score,

                    certification_score=(
                        certification_score
                    ),
                )
            )


            # =============================
            # MANDATORY SKILLS
            # =============================

            mandatory_result = (
                check_mandatory_skills(

                    required_skills,

                    matched_skills
                )
            )


            missing_mandatory = (
                mandatory_result[
                    "missing_mandatory"
                ]
            )


            # =============================
            # APPLY PENALTY
            # =============================

            final_score = (
                apply_mandatory_penalty(

                    final_score,

                    missing_mandatory
                )
            )


            # =============================
            # RECOMMENDATION
            # =============================

            recommendation = (
                get_recommendation(
                    final_score
                )
            )


            # =============================
            # STORE RESULT
            # =============================

            candidates.append({

                "filename": filename,

                "score": final_score,

                "skill_score": skill_score,

                "semantic_score": (
                    semantic_score
                ),

                "experience_score": (
                    experience_score
                ),

                "preferred_score": (
                    preferred_score
                ),

                "education_score": (
                    education_score
                ),

                "certification_score": (
                    certification_score
                ),

                "candidate_experience_years": (
                    candidate_experience
                ),

                "required_experience_years": (
                    required_experience
                ),

                "matched_skills": (
                    matched_skills
                ),

                "missing_skills": (
                    missing_skills
                ),

                "preferred_skills": (
                    preferred_skills
                ),

                "education": education,

                "missing_mandatory": (
                    missing_mandatory
                ),

                "recommendation": (
                    recommendation
                ),
            })


            successful += 1


        except Exception as exc:

            errors.append(
                f"{filename}: {str(exc)}"
            )


        finally:

            # =============================
            # DELETE TEMP FILE
            # =============================

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )


    # =====================================
    # SORT CANDIDATES
    # =====================================

    candidates.sort(

        key=lambda candidate:
            candidate["score"],

        reverse=True
    )


    # =====================================
    # TOP 5
    # =====================================

    top_5 = candidates[:5]


    # =====================================
    # ASSIGN RANK
    # =====================================

    for index, candidate in enumerate(

        top_5,

        start=1

    ):

        candidate["rank"] = index


    # =====================================
    # RETURN RESPONSE
    # =====================================

    return {

        "total_resumes": len(
            resumes
        ),

        "successful_resumes": (
            successful
        ),

        "failed_resumes": (
            len(resumes) - successful
        ),

        "required_skills": (
            required_skills
        ),

        "preferred_skills": (
            preferred_skills
        ),

        "required_experience_years": (
            required_experience
        ),

        "top_5": top_5,

        "errors": errors,
    }
