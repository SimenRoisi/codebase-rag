# chunking/code_chunker.py

from dataclasses import dataclass
from typing import List, Dict
import hashlib

from parsing.python_parser import CodeUnit


@dataclass
class Chunk:
    id: str
    text: str
    metadata: Dict
    embedding: List[float] = None 


def build_chunk_text(unit: CodeUnit) -> str:
    """
    Convert a CodeUnit into structured text for embeddings.
    """

    imports_text = "\n".join(unit.imports) if unit.imports else "None"
    docstring_text = unit.docstring if unit.docstring else "None"

    text = f"""
Repository: {unit.repo}

File: {unit.file}

Type: {unit.type}

Name: {unit.name}

Imports:
{imports_text}

Docstring:
{docstring_text}

Code:
{unit.code}
"""

    return text.strip()


def generate_chunk_id(unit: CodeUnit) -> str:
    """
    Generate a stable chunk ID using repo + file + name.
    """

    base_string = f"{unit.repo}:{unit.file}:{unit.name}:{unit.type}"

    return hashlib.md5(base_string.encode()).hexdigest()


def codeunits_to_chunks(units: List[CodeUnit]) -> List[Chunk]:
    """
    Convert CodeUnits into Chunks.
    """

    chunks: List[Chunk] = []

    for unit in units:

        chunk_text = build_chunk_text(unit)

        chunk = Chunk(
            id=generate_chunk_id(unit),
            text=chunk_text,
            metadata={
                "repo": unit.repo,
                "file": unit.file,
                "type": unit.type,
                "name": unit.name,
            },
        )

        chunks.append(chunk)

    return chunks