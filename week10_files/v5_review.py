import csv
from pathlib import Path


def load_scores(path: str | Path) -> tuple[list[tuple[str, float]], list[str]]:
    # 1. 파일이 있는지 확인하고, 경로 오류는 호출자에게 알린다.
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    scores: list[tuple[str, float]] = []
    skipped: list[str] = []
    seen_names: set[str] = set()

    with file_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file, strict=True)
        # 2. 헤더를 확인한 뒤 데이터 처리에서 제외한다.
        header = next(reader, None)
        if header is None or [column.strip() for column in header] != ["name", "score"]:
            raise ValueError("CSV header must be: name,score")

        # 3. CSV 행을 읽고 열 개수가 맞는지 확인한다.
        previous_line_number = reader.line_num
        for row in reader:
            line_number = previous_line_number + 1
            previous_line_number = reader.line_num
            issue = None

            if len(row) != 2:
                issue = "expected exactly 2 columns"
            else:
                name, raw_score = (value.strip() for value in row)
                # 4. 이름, 빈 점수, 숫자 형식, 범위, 중복 이름을 검증한다.
                if not name:
                    issue = "name is empty"
                elif not raw_score:
                    issue = "score is empty"
                else:
                    try:
                        score = float(raw_score)
                    except ValueError:
                        issue = "score is not numeric"
                    else:
                        if not 0 <= score <= 100:
                            issue = "score must be between 0 and 100"
                        elif name in seen_names:
                            issue = "duplicate name"

            # 5. 검증에 실패한 행은 줄 번호와 사유를 기록하고 건너뛴다.
            if issue is not None:
                skipped.append(f"line {line_number}: {issue}")
                continue

            seen_names.add(name)
            scores.append((name, score))

    # 6. 유효한 성적과 건너뛴 행 기록을 함께 반환한다.
    return scores, skipped