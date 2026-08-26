from app.agents.jd_analyzer import normalize_text


def find_matching_skills(
    resume_text: str,
    required_skills: list[str],
) -> dict:
    normalized_resume = normalize_text(resume_text)

    matched = []
    missing = []

    for skill in required_skills:
        if skill in normalized_resume:
            matched.append(skill)
        else:
            missing.append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
    }

