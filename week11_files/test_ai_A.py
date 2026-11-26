import pytest

from load_scores import load_scores


def test_loads_valid_scores_and_keeps_duplicate_names(tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_bytes(
        b"\xef\xbb\xbfname,score\n"
        b"  Kim Hana  , 0 \n"
        b"Kim Hana,100\n"
        b'"Lee, Min",75\n'
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Kim Hana", 0), ("Kim Hana", 100), ("Lee, Min", 75)]
    assert skipped == []


def test_returns_empty_lists_for_header_only_file(tmp_path):
    csv_path = tmp_path / "header_only.csv"
    csv_path.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_path) == ([], [])


def test_skips_invalid_rows_with_reasons_and_line_numbers(tmp_path):
    csv_path = tmp_path / "mixed.csv"
    csv_path.write_text(
        "name,score\n"
        "\n"
        ",80\n"
        "Kim,\n"
        "Park,absent\n"
        "Lee,-1\n"
        "Oh,101\n"
        "Too,many,columns\n"
        "OnlyOne\n"
        "Good,50\n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Good", 50)]
    assert skipped == [
        (3, ",80", "이름이 비어 있음"),
        (4, "Kim,", "점수가 비어 있음"),
        (5, "Park,absent", "점수가 정수가 아님"),
        (6, "Lee,-1", "점수가 0~100 밖"),
        (7, "Oh,101", "점수가 0~100 밖"),
        (8, "Too,many,columns", "열 개수가 2가 아님"),
        (9, "OnlyOne", "열 개수가 2가 아님"),
    ]


def test_raises_file_not_found_error_for_missing_file(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(missing_path)