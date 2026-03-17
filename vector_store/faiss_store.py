# vector_store/faiss_store.py

import faiss
import numpy as np
import os
import pickle
from typing import List, Dict

from chunking.code_chunker import Chunk

FAISS_INDEX_FILE = "data/faiss_index/faiss.index"
FAISS_METADATA_FILE = "data/faiss_index/metadata.pkl"


class FaissStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata: List[Dict] = []

        os.makedirs(os.path.dirname(FAISS_INDEX_FILE), exist_ok=True)

    def add_chunks(self, chunks: List[Chunk]):
        """
        Legg til chunks i FAISS index.
        """
        vectors = np.array([c.embedding for c in chunks], dtype='float32')
        self.index.add(vectors)

        self.metadata.extend([
            {
            "text": c.text,
            "metadata": c.metadata
            } for c in chunks
        ])

    def save(self):
        """
        Lagre index + metadata.
        """
        faiss.write_index(self.index, FAISS_INDEX_FILE)
        with open(FAISS_METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """
        Last index + metadata.
        """
        if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(FAISS_METADATA_FILE):
            self.index = faiss.read_index(FAISS_INDEX_FILE)
            with open(FAISS_METADATA_FILE, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            print("No existing FAISS index found.")

    def search(self, query_vector: List[float], top_k: int = 5):
        """
        Finn top_k nærmeste chunks til query_vector.
        """
        xq = np.array([query_vector], dtype='float32')
        distances, indices = self.index.search(xq, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                results.append({
                    "distance": float(dist),
                    "text": self.metadata[idx]["text"],
                    "metadata": self.metadata[idx]["metadata"]
                })
        return results