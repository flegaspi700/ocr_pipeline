import io
from pathlib import Path
from typing import Iterable, List

from PIL import Image
import fitz

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif"}


def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def load_image(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")
    if not is_image_file(path):
        raise ValueError(f"Unsupported image file type: {path}")
    return Image.open(path).convert("RGB")


def rasterize_pdf(path: Path, dpi: int = 200) -> List[Image.Image]:
    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported PDF file type: {path}")

    document = fitz.open(path)
    images: List[Image.Image] = []
    matrix = fitz.Matrix(dpi / 72, dpi / 72)

    for page in document:
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        image_bytes = pix.tobytes("png")
        images.append(Image.open(io.BytesIO(image_bytes)).convert("RGB"))

    return images


def load_inputs(paths: Iterable[Path], dpi: int = 200) -> List[tuple[Path, Image.Image]]:
    loaded = []
    for path in paths:
        if is_image_file(path):
            loaded.append((path, load_image(path)))
        elif path.suffix.lower() == ".pdf":
            for index, image in enumerate(rasterize_pdf(path, dpi=dpi), start=1):
                page_path = Path(f"{path.stem}_page_{index}.png")
                loaded.append((page_path, image))
        else:
            raise ValueError(f"Unsupported input file: {path}")
    return loaded
