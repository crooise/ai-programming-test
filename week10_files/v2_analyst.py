import csv


def load_scores(path: str) -> list[tuple[str, float]]:
    scores = []
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["name", "score"]:
            raise ValueError("CSV header must be: name,score")

        for row in reader:
            name = row["name"].strip()
            score = float(row["score"])
            scores.append((name, score))

    return scores