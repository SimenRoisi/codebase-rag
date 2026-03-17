from embedding.embedding_model import EmbeddingModel
from vector_store.faiss_store import FaissStore
from retrieval.retriever import Retriever


# last eksisterende FAISS index
store = FaissStore()
store.load()

model = EmbeddingModel()

retriever = Retriever(model, store)

query = "Where is weather data fetched?"

results = retriever.retrieve(query, top_k=3)

for i, r in enumerate(results, 1):
    print("=" * 80)
    print(f"Chunk #{i}")
    print(f"Distance: {r['distance']:.4f}")
    # Kortversjon: docstring + kode
    text = r['text']
    # split text på "Code:" og hent kun docstring + kode
    parts = text.split("Code:")
    if len(parts) == 2:
        doc_and_code = parts[1].strip()
    else:
        doc_and_code = text.strip()
    print(doc_and_code)
    print("\n")