import re


SKILL_ALIASES = {
    "python": [
        "python",
    ],
    "java": [
        "java",
    ],
    "javascript": [
        "javascript",
        "js",
    ],
    "typescript": [
        "typescript",
        "ts",
    ],
    "react": [
        "react",
        "react.js",
        "reactjs",
    ],
    "angular": [
        "angular",
    ],
    "node.js": [
        "node.js",
        "nodejs",
        "node js",
    ],
    "fastapi": [
        "fastapi",
    ],
    "django": [
        "django",
    ],
    "flask": [
        "flask",
    ],
    "spring": [
        "spring framework",
        "spring boot",
    ],
    "rest api": [
        "rest api",
        "restful api",
        "restful web services",
        "rest services",
    ],
    "graphql": [
        "graphql",
    ],
    "postgresql": [
        "postgresql",
        "postgres",
    ],
    "mysql": [
        "mysql",
    ],
    "mongodb": [
        "mongodb",
        "mongo db",
        "mongo",
    ],
    "redis": [
        "redis",
    ],
    "sql": [
        "sql",
    ],
    "docker": [
        "docker",
        "dockerized",
        "containerization",
    ],
    "kubernetes": [
        "kubernetes",
        "k8s",
    ],
    "aws": [
        "aws",
        "amazon web services",
    ],
    "azure": [
        "azure",
        "microsoft azure",
    ],
    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform",
    ],
    "git": [
        "git",
    ],
    "github": [
        "github",
    ],
    "jenkins": [
        "jenkins",
    ],
    "terraform": [
        "terraform",
    ],
    "microservices": [
        "microservices",
        "microservices architecture",
    ],
    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml",
    ],
    "deep learning": [
        "deep learning",
        "deep-learning",
    ],
}


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def extract_skills(
    text: str,
) -> list[str]:

    normalized_text = normalize_text(
        text
    )

    found_skills = []

    for canonical_skill, aliases in (
        SKILL_ALIASES.items()
    ):

        for alias in aliases:

            normalized_alias = normalize_text(
                alias
            )

            if normalized_alias in normalized_text:

                found_skills.append(
                    canonical_skill
                )

                break

    return sorted(
        list(set(found_skills))
    )


def extract_experience_years(
    text: str,
) -> float:

    normalized_text = text.lower()

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of)?\s*experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s*exp",
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            normalized_text,
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


def extract_education(
    text: str,
) -> list[str]:

    normalized_text = normalize_text(
        text
    )

    education_keywords = [
        "bachelor",
        "bachelors",
        "b.tech",
        "btech",
        "b.e",
        "be degree",
        "master",
        "masters",
        "m.tech",
        "mtech",
        "m.e",
        "mba",
        "mca",
        "bca",
        "phd",
        "doctorate",
    ]

    found = []

    for keyword in education_keywords:

        if keyword in normalized_text:

            found.append(keyword)

    return sorted(
        list(set(found))
    )
