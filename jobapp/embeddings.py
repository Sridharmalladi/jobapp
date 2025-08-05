from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once at module level (so it loads only once when imported)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    """
    Generate embedding vector for a single text input.

    Args:
        text (str): Input text to embed

    Returns:
        np.ndarray: Embedding vector (768-dimensional)
    """
    # Encode returns a numpy array of embeddings
    embedding = model.encode(text)
    return embedding

def get_embeddings(texts: list[str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts.

    Args:
        texts (list[str]): List of strings

    Returns:
        np.ndarray: 2D array where each row is an embedding vector
    """
    embeddings = model.encode(texts)
    return embeddings
