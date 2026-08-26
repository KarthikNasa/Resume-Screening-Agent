import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\- ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(job_description: str) -> list[str]:
    """
    Basic skill extraction for the MVP.

    We'll improve this later using semantic/LLM-based extraction.
    """

    known_skills = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "angular",
        "node.js",
        "fastapi",
        "django",
        "flask",
        "spring",
        "rest api",
        "graphql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "github",
        "jenkins",
        "terraform",
        "microservices",
        "machine learning",
        "deep learning",
        "sql",
    ]

    normalized_jd = normalize_text(job_description)

    found_skills = []

    for skill in known_skills:
        if skill in normalized_jd:
            found_skills.append(skill)

    return found_skills

