import csv


def load_scores(path: str) -> list[tuple[str, float]]:
    scores = []
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header != ["name", "score"]:
            raise ValueError("CSV header must be: name,score")

        for line_number, row in enumerate(reader, start=2):
            if len(row) != 2:
                raise ValueError(f"line {line_number}: expected 2 columns")

            name, raw_score = row
            try:
                score = float(raw_score)
            except ValueError as error:
                raise ValueError(f"line {line_number}: score must be numeric") from error
            scores.append((name.strip(), score))

    return scores