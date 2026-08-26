def check_mandatory_skills(
    required_skills: list[str],
    matched_skills: list[str],
) -> dict:

    required = set(
        required_skills
    )

    matched = set(
        matched_skills
    )

    missing = sorted(
        list(
            required - matched
        )
    )

    return {
        "has_missing_mandatory": (
            len(missing) > 0
        ),
        "missing_mandatory": missing,
    }


def apply_mandatory_penalty(
    score: float,
    missing_mandatory: list[str],
) -> float:

    if not missing_mandatory:
        return score

    # Penalize each missing mandatory skill.
    penalty = len(
        missing_mandatory
    ) * 10

    return round(
        max(
            score - penalty,
            0,
        ),
        2,
    )
