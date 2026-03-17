from parsing.python_parser import parse_python_file

with open("/Users/simenroisi/Documents/PROJECT/WeatherETL/app/etl/extract.py", "r", encoding="utf-8") as f:
    code = f.read()

units = parse_python_file(
    repo_name="WeatherETL",
    file_path="extract.py",
    code=code
)

for u in units:
    print(f"{u.type} {u.name}")
    print(f"Docstring: {u.docstring}")
    # kun print første 50 tegn av kode for oversikt
    print(f"Code preview: {u.code[:50].replace('\\n',' ')}...")
    print("-" * 40)