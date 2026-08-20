from pathlib import Path

from PIL import Image

from src.schemas.image import ImageInput


def load_image(image: ImageInput) -> Image.Image:
    """Load an image selected locally by the admin."""

    if image.source == "local":
        return _load_local_image(image.identifier)

    raise ValueError(
        f"Unsupported image source: {image.source}. Only local files are supported."
    )


def _load_local_image(image_path: str) -> Image.Image:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    return Image.open(path)
