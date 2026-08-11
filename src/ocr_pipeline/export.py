import csv
import json
from pathlib import Path
from typing import Any, Dict, List


def export_to_json(results: List[Dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(results, handle, ensure_ascii=False, indent=2)


def export_to_csv(results: List[Dict[str, Any]], output_path: Path) -> None:
    if not results:
        raise ValueError("No results available to export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for item in results for key in item})

    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
