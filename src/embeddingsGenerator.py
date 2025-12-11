from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class embeddingsGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, doc_chunks: List[str]) -> np.ndarray:
        texts = [
            doc.page_content if hasattr(doc, "page_content") else str(doc)
            for doc in doc_chunks
        ]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings
