# ingestion/repo_loader.py

from pathlib import Path
from git import Repo
from typing import List

from parsing.python_parser import parse_python_file, CodeUnit


def clone_or_update_repo(repo_url: str, repo_name: str) -> Path:
    """
    Clone repo if it doesn't exist.
    Otherwise pull latest changes.
    """

    base_path = Path("data/repos")
    base_path.mkdir(parents=True, exist_ok=True)

    repo_path = base_path / repo_name

    if not repo_path.exists():
        print(f"Cloning {repo_url} into {repo_path}")
        Repo.clone_from(repo_url, repo_path)
    else:
        print(f"Updating existing repo at {repo_path}")
        repo = Repo(repo_path)
        repo.remotes.origin.pull()

    return repo_path


def parse_repository(repo_path: Path, repo_name: str) -> List[CodeUnit]:
    """
    Find all Python files and parse them into CodeUnits.
    """

    code_units: List[CodeUnit] = []

    py_files = list(repo_path.rglob("*.py"))

    print(f"Found {len(py_files)} Python files.")

    for py_file in py_files:

        try:
            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            print(f"Could not read {py_file}: {e}")
            continue

        relative_path = py_file.relative_to(repo_path)

        units = parse_python_file(
            repo_name=repo_name,
            file_path=str(relative_path),
            code=code
        )

        code_units.extend(units)

    return code_units


def clone_and_parse_repo(repo_url: str, repo_name: str) -> List[CodeUnit]:
    """
    Full pipeline:
    clone/update repo -> parse Python files
    """

    repo_path = clone_or_update_repo(repo_url, repo_name)

    code_units = parse_repository(repo_path, repo_name)

    return code_units