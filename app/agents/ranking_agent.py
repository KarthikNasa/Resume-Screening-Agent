from app.services.scoring import calculate_skill_score


def rank_candidates(
    candidates: list[dict],
    required_skills: list[str],
) -> list[dict]:

    ranked = []

    for candidate in candidates:

        matched_skills = candidate.get(
            "matched_skills",
            [],
        )

        score = calculate_skill_score(
            matched_skills,
            required_skills,
        )

        candidate["score"] = score

        ranked.append(candidate)

    ranked.sort(
        key=lambda candidate: candidate["score"],
        reverse=True,
    )

    return ranked

