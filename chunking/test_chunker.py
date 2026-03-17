from ingestion.repo_loader import clone_and_parse_repo
from chunking.code_chunker import codeunits_to_chunks


units = clone_and_parse_repo(
    "https://github.com/SimenRoisi/WeatherETL.git",
    "WeatherETL"
)

chunks = codeunits_to_chunks(units)

print(f"Units: {len(units)}")
print(f"Chunks: {len(chunks)}")

print("\nExample chunk:\n")
print(chunks[0].text)