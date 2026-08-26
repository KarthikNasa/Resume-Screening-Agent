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
        "spring",
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


def extract_skills(job_description: str) -> list[str]:
    normalized_jd = normalize_text(
        job_description
    )

    found_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            normalized_alias = normalize_text(
                alias
            )

            if normalized_alias in normalized_jd:
                found_skills.append(
                    canonical_skill
                )

                break

    return sorted(
        list(set(found_skills))
    )
