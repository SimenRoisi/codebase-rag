from ingestion.repo_loader import clone_and_parse_repo

repo_url = "https://github.com/SimenRoisi/WeatherETL.git"
repo_name = "WeatherETL"

units = clone_and_parse_repo(repo_url, repo_name)

print(f"Total units parsed: {len(units)}")

for u in units[:10]:  # vis de første 10 units
    print(f"{u.type} {u.name} ({u.file})")