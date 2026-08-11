import argparse
from io import BytesIO
from pathlib import Path

from .backend import BaiduUnlimitedOCRBackend, OCRBackend
from .export import export_to_csv, export_to_json
from .io import load_inputs
from .preprocess import preprocess_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OCR pipeline on image and PDF files.")
    parser.add_argument("inputs", nargs="+", help="Paths to image or PDF files.")
    parser.add_argument("--output", required=True, help="Output path for results.")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format.")
    parser.add_argument("--dpi", type=int, default=200, help="Rasterization DPI for PDF pages.")
    parser.add_argument("--backend", choices=["baidu"], default="baidu", help="OCR backend to use.")
    parser.add_argument("--threshold", type=int, default=128, help="Binarization threshold for preprocessing.")
    return parser


def get_backend(name: str) -> OCRBackend:
    if name == "baidu":
        return BaiduUnlimitedOCRBackend()
    raise ValueError(f"Unsupported backend: {name}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    input_paths = [Path(path) for path in args.inputs]
    loaded = load_inputs(input_paths, dpi=args.dpi)
    backend = get_backend(args.backend)

    results = []
    for path, image in loaded:
        processed = preprocess_image(image, threshold=args.threshold)
        buffer = BytesIO()
        processed.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        ocr_data = backend.recognize(image_bytes)
        results.append({
            "source": str(path),
            "results": ocr_data,
        })

    output_path = Path(args.output)
    if args.format == "json":
        export_to_json(results, output_path)
    else:
        export_to_csv(results, output_path)


if __name__ == "__main__":
    main()
