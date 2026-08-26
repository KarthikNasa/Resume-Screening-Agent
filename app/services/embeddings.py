from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    """
    Load the embedding model once and reuse it.

    The first request downloads the model.
    Later requests reuse the loaded model.
    """

    return SentenceTransformer(MODEL_NAME)


def create_embedding(text: str) -> np.ndarray:
    """
    Convert text into a semantic embedding.
    """

    model = get_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding


def calculate_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Calculate cosine similarity between two texts.

    Returns a score from approximately 0 to 1.
    """

    model = get_model()

    embeddings = model.encode(
        [text_a, text_b],
        normalize_embeddings=True,
    )

    similarity = float(
        np.dot(
            embeddings[0],
            embeddings[1],
        )
    )

    return max(
        0.0,
        min(1.0, similarity),
    )


def similarity_percentage(
    text_a: str,
    text_b: str,
) -> float:

    similarity = calculate_similarity(
        text_a,
        text_b,
    )

    return round(
        similarity * 100,
        2,
    )

