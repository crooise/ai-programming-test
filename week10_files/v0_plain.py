import csv


def load_scores(path: str) -> list[tuple[str, int]]:
    with open(path, newline="", encoding="utf-8-sig") as file:
        rows = csv.DictReader(file)
        return [(row["name"], int(row["score"])) for row in rows]