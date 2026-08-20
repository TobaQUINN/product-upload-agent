import json
from pathlib import Path

from src.schemas.image import ImageInput
from src.schemas.product import ProductDraft


OUTPUT_DIR = Path("output")


def save_product_draft(
    draft: ProductDraft,
    image: ImageInput,
) -> Path:
    """
    Save a ProductDraft as a JSON file in the output directory.

    The image identifier is used to determine the output filename.
    """

    OUTPUT_DIR.mkdir(exist_ok=True)

    image_name = Path(image.identifier).stem
    output_path = OUTPUT_DIR / f"{image_name}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            draft.model_dump(),
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_path
