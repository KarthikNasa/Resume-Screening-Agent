def calculate_skill_score(
    matched_skills: list[str],
    required_skills: list[str],
) -> float:

    if not required_skills:
        return 0.0

    score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return round(score, 2)


def calculate_final_score(
    skill_score: float,
    semantic_score: float,
) -> float:
    """
    Calculate the overall candidate score.

    Skill match: 40%
    Semantic match: 30%

    The remaining 30% will be added in later stages.
    """

    final_score = (
        skill_score * 0.40
        + semantic_score * 0.30
    )

    return round(
        final_score,
        2,
    )


def get_recommendation(
    score: float,
) -> str:

    if score >= 85:
        return "Excellent Match"

    if score >= 70:
        return "Strong Match"

    if score >= 55:
        return "Good Match"

    if score >= 40:
        return "Partial Match"

    return "Weak Match"
