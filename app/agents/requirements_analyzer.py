import re

from app.agents.jd_analyzer import (
    extract_skills,
    normalize_text,
)


def extract_required_skills(
    job_description: str,
) -> list[str]:

    text = normalize_text(
        job_description
    )

    required_section = text

    required_markers = [
        "required skills",
        "requirements",
        "must have",
        "mandatory",
        "required",
    ]

    preferred_markers = [
        "preferred",
        "nice to have",
        "good to have",
        "bonus",
    ]

    # Try to isolate the required section.
    for marker in required_markers:

        if marker in text:

            parts = text.split(
                marker,
                1,
            )

            if len(parts) == 2:

                required_section = parts[1]

                break

    # Remove preferred section if found.
    for marker in preferred_markers:

        if marker in required_section:

            required_section = (
                required_section.split(
                    marker,
                    1,
                )[0]
            )

    return extract_skills(
        required_section
    )


def extract_preferred_skills(
    job_description: str,
) -> list[str]:

    text = normalize_text(
        job_description
    )

    preferred_text = ""

    preferred_markers = [
        "preferred",
        "nice to have",
        "good to have",
        "bonus",
    ]

    for marker in preferred_markers:

        if marker in text:

            parts = text.split(
                marker,
                1,
            )

            if len(parts) == 2:

                preferred_text = parts[1]

                break

    if not preferred_text:

        return []

    return extract_skills(
        preferred_text
    )


def extract_minimum_experience(
    job_description: str,
) -> float:

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?",
        r"minimum\s*(?:of)?\s*(\d+(?:\.\d+)?)",
    ]

    values = []

    text = normalize_text(
        job_description
    )

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
        )

        for match in matches:

            try:

                values.append(
                    float(match)
                )

            except ValueError:
                pass

    if not values:
        return 0.0

    return max(values)
