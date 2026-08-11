import json
from pathlib import Path

from ocr_pipeline.export import export_to_csv, export_to_json


def test_export_to_json(tmp_path: Path) -> None:
    results = [{"source": "sample.png", "text": "hello"}]
    output_path = tmp_path / "results.json"
    export_to_json(results, output_path)

    with open(output_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    assert payload == results


def test_export_to_csv(tmp_path: Path) -> None:
    results = [{"source": "sample.png", "text": "hello"}]
    output_path = tmp_path / "results.csv"
    export_to_csv(results, output_path)

    text = output_path.read_text(encoding="utf-8")
    assert "source" in text
    assert "text" in text
    assert "hello" in text
