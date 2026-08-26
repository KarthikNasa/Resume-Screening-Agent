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


def get_recommendation(score: float) -> str:

    if score >= 90:
        return "Excellent Match"

    if score >= 75:
        return "Strong Match"

    if score >= 60:
        return "Good Match"

    if score >= 40:
        return "Partial Match"

    return "Weak Match"
