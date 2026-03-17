# retrieval/retriever.py

from typing import List, Dict

from embedding.embedding_model import EmbeddingModel
from vector_store.faiss_store import FaissStore


class Retriever:
    def __init__(self, embedding_model: EmbeddingModel, store: FaissStore):
        self.embedding_model = embedding_model
        self.store = store

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Given a query, return top_k most relevant chunks.
        """

        # 1. embed query
        query_embedding = self.embedding_model.embed_texts([query])[0]

        # 2. search FAISS
        results = self.store.search(query_embedding, top_k=top_k)

        return results