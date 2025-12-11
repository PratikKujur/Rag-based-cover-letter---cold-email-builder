from src.vectorstore import vectorStore
from src.embeddingsGenerator import embeddingsGenerator
from typing import List, Tuple


class Ragpipeline:
    def __init__(
        self, vector_store: vectorStore, embeddings_generator: embeddingsGenerator
    ):
        self.vector_store = vector_store
        self.embeddings_generator = embeddings_generator

    def query(self, query_text: str, top_k: int = 5) -> List[Tuple[str, float]]:
        query_embedding = self.embeddings_generator.model.encode([query_text])[0]
        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()], n_results=top_k
        )

        retrieved_docs = results["documents"][0]
        scores = results["distances"][0]

        return list(zip(retrieved_docs, scores))
