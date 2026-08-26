from app.agents.jd_analyzer import (
    SKILL_ALIASES,
    normalize_text,
)


def find_matching_skills(
    resume_text: str,
    required_skills: list[str],
) -> dict:

    normalized_resume = normalize_text(
        resume_text
    )

    matched = []
    missing = []

    for skill in required_skills:

        aliases = SKILL_ALIASES.get(
            skill,
            [skill],
        )

        found = False

        for alias in aliases:

            normalized_alias = normalize_text(
                alias
            )

            if normalized_alias in normalized_resume:
                found = True
                break

        if found:
            matched.append(skill)
        else:
            missing.append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
    }
