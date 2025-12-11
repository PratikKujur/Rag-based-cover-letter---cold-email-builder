import numpy as np
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Any


class vectorStore:
    def __init__(
        self, collection_name: str = "resume_job_descriptions", dir: str = None
    ):
        self.client = chromadb.Client(
            Settings(
                persist_directory=dir,
            )
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_embeddings(self, doc_chunks: List[Any], embeddings: np.ndarray):
        # Validate lengths
        if doc_chunks is None or embeddings is None:
            raise ValueError("doc_chunks and embeddings must be provided")

        if len(doc_chunks) != len(embeddings):
            print(
                f"Length of docs not equal to length of embeddings,lengths are {len(doc_chunks)} and {len(embeddings)} respectively"
            )
            return

        documents_text = []
        embeddings_list = []

        for doc, emb in zip(doc_chunks, embeddings):
            # Support both Document objects and plain strings
            text = doc.page_content if hasattr(doc, "page_content") else str(doc)
            documents_text.append(text)

            # Ensure embedding is a plain list of floats
            if hasattr(emb, "tolist"):
                embeddings_list.append(emb.tolist())
            else:
                embeddings_list.append(list(emb))

        ids = [str(uuid.uuid4()) for _ in range(len(documents_text))]
        self.collection.add(
            documents=documents_text, embeddings=embeddings_list, ids=ids
        )
