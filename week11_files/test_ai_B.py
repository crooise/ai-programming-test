import pytest

from load_scores import load_scores


def test_loads_valid_rows_including_score_boundaries_and_comma_name(tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(
        "name,score\n"
        "  김하나  ,0\n"
        '"최, 네번",100\n'
        "김하나,88\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("김하나", 0), ("최, 네번", 100), ("김하나", 88)]
    assert skipped == []


@pytest.mark.parametrize("contents", ["", "name,score\n"])
def test_returns_empty_lists_for_empty_or_header_only_file(tmp_path, contents):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text(contents, encoding="utf-8")

    assert load_scores(csv_path) == ([], [])


def test_reports_each_invalid_row_with_line_number_and_reason(tmp_path):
    csv_path = tmp_path / "mixed.csv"
    csv_path.write_text(
        "name,score\n"
        ",80\n"
        "Kim,   \n"
        "Park,absent\n"
        "Lee,-1\n"
        "Oh,101\n"
        "Too,many,columns\n"
        "OnlyOne\n"
        "Good,50\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Good", 50)]
    assert skipped == [
        (2, ",80", "이름이 비어 있음"),
        (3, "Kim,   ", "점수가 비어 있음"),
        (4, "Park,absent", "점수가 정수가 아님"),
        (5, "Lee,-1", "점수가 0~100 밖"),
        (6, "Oh,101", "점수가 0~100 밖"),
        (7, "Too,many,columns", "열 개수가 2가 아님"),
        (8, "OnlyOne", "열 개수가 2가 아님"),
    ]


def test_raises_file_not_found_error_for_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_raises_os_error_when_path_is_a_directory(tmp_path):
    with pytest.raises(OSError):
        load_scores(tmp_path)