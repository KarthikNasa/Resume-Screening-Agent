def calculate_skill_score(
    matched_skills: list[str],
    required_skills: list[str],
) -> float:

    if not required_skills:
        return 100.0

    score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return round(
        score,
        2,
    )


def calculate_experience_score(
    candidate_years: float,
    required_years: float,
) -> float:

    if required_years <= 0:
        return 100.0

    if candidate_years <= 0:
        return 0.0

    score = (
        candidate_years
        / required_years
    ) * 100

    return round(
        min(score, 100),
        2,
    )


def calculate_preferred_score(
    matched_skills: list[str],
    preferred_skills: list[str],
) -> float:

    if not preferred_skills:
        return 100.0

    matched = set(
        matched_skills
    )

    preferred = set(
        preferred_skills
    )

    count = len(
        matched.intersection(
            preferred
        )
    )

    score = (
        count
        / len(preferred)
    ) * 100

    return round(
        score,
        2,
    )


def calculate_education_score(
    education: list[str],
) -> float:

    if education:
        return 100.0

    return 50.0


def calculate_certification_score(
    resume_text: str,
) -> float:

    text = resume_text.lower()

    certification_keywords = [
        "certified",
        "certification",
        "certificate",
        "aws certified",
        "azure certified",
        "google certified",
        "pmp",
        "scrum master",
        "cissp",
    ]

    for keyword in certification_keywords:

        if keyword in text:
            return 100.0

    return 0.0


def calculate_final_score(
    skill_score: float,
    semantic_score: float,
    experience_score: float,
    preferred_score: float,
    education_score: float,
    certification_score: float,
) -> float:

    score = (
        skill_score * 0.35
        + semantic_score * 0.25
        + experience_score * 0.20
        + preferred_score * 0.10
        + education_score * 0.05
        + certification_score * 0.05
    )

    return round(
        score,
        2,
    )


def get_recommendation(
    score: float,
) -> str:

    if score >= 85:
        return "Excellent Match"

    if score >= 75:
        return "Strong Match"

    if score >= 60:
        return "Good Match"

    if score >= 45:
        return "Partial Match"

    return "Weak Match"
