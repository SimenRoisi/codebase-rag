# vector_store/test_faiss.py

from ingestion.repo_loader import clone_and_parse_repo
from chunking.code_chunker import codeunits_to_chunks
from embedding.embedding_model import EmbeddingModel
from vector_store.faiss_store import FaissStore

# 1. hent repo + chunker
units = clone_and_parse_repo("https://github.com/SimenRoisi/WeatherETL.git", "WeatherETL")
chunks = codeunits_to_chunks(units)

# 2. lag embeddings
texts = [c.text for c in chunks]
model = EmbeddingModel()
embeddings = model.embed_texts(texts)

for c, e in zip(chunks, embeddings):
    c.embedding = e

# 3. legg inn i FAISS
store = FaissStore(dimension=len(embeddings[0]))
store.add_chunks(chunks)
store.save()

# 4. prøv et søk
query = "fetch weather data from API"
q_emb = model.embed_texts([query])[0]

results = store.search(q_emb, top_k=3)

for r in results:
    print(r)