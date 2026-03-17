from ingestion.repo_loader import clone_and_parse_repo
from chunking.code_chunker import codeunits_to_chunks
from embedding.embedding_model import EmbeddingModel


units = clone_and_parse_repo(
    "https://github.com/SimenRoisi/WeatherETL.git",
    "WeatherETL"
)

chunks = codeunits_to_chunks(units)

texts = [c.text for c in chunks]

model = EmbeddingModel()

embeddings = model.embed_texts(texts)

print("Chunks:", len(chunks))
print("Embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))