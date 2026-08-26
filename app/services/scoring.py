def calculate_skill_score(
    matched_skills: list[str],
    required_skills: list[str],
) -> float:

    if not required_skills:
        return 0.0

    score = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return round(score, 2)

