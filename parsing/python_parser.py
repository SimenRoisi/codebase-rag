# parsing/python_parser.py

import ast
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CodeUnit:
    repo: str
    file: str
    type: str              # 'function', 'class', 'method'
    name: str
    code: str
    docstring: Optional[str]
    imports: List[str] = field(default_factory=list)  # alle imports fra filen


def get_node_source(code: str, node: ast.AST) -> str:
    """Hent kildekode for en AST-node, fallback hvis ast.unparse ikke finnes"""
    try:
        return ast.unparse(node)
    except AttributeError:
        lines = code.splitlines()
        start = node.lineno - 1
        end = getattr(node, "end_lineno", node.lineno)
        return "\n".join(lines[start:end])


def extract_imports(code: str) -> List[str]:
    """Returner en liste med alle import-strenger fra koden"""
    imports = []
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    imports.append(f"import {alias.name} as {alias.asname}")
                else:
                    imports.append(f"import {alias.name}")

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names_list = [alias.name + (f" as {alias.asname}" if alias.asname else "") for alias in node.names]
            # Lag én entry per import-element
            for name in names_list:
                imports.append(f"from {module} import {name}")

    return imports


def parse_python_file(repo_name: str, file_path: str, code: str) -> List[CodeUnit]:
    """Parser en Python-fil og returnerer funksjoner, klasser og metoder som CodeUnit-objekter"""
    code_units: List[CodeUnit] = []
    imports = extract_imports(code)

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code_units

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_code = get_node_source(code, node)
            docstring = ast.get_docstring(node)
            unit = CodeUnit(
                repo=repo_name,
                file=file_path,
                type="function",
                name=node.name,
                code=function_code,
                docstring=docstring,
                imports=imports
            )
            code_units.append(unit)

        elif isinstance(node, ast.ClassDef):
            class_code = get_node_source(code, node)
            docstring = ast.get_docstring(node)
            unit = CodeUnit(
                repo=repo_name,
                file=file_path,
                type="class",
                name=node.name,
                code=class_code,
                docstring=docstring,
                imports=imports
            )
            code_units.append(unit)

            # Legg til methods i klassen
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_code = get_node_source(code, child)
                    method_doc = ast.get_docstring(child)
                    method_unit = CodeUnit(
                        repo=repo_name,
                        file=file_path,
                        type="method",
                        name=f"{node.name}.{child.name}",
                        code=method_code,
                        docstring=method_doc,
                        imports=imports
                    )
                    code_units.append(method_unit)

    return code_units