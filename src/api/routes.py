from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from src.ai_agent.batch_processor import process_batch


router = APIRouter()
UPLOAD_DIR = Path("input") / "uploads"


@router.post("/process")
def process_products(
    images: list[UploadFile] = File(
        ...,
        description="Select one or more product images to process."
    )
):
    """
    Process a batch of image files selected by the admin.
    """

    image_paths = []

    for image in images:
        suffix = Path(image.filename or "upload.img").suffix
        image_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
        image_path.parent.mkdir(parents=True, exist_ok=True)

        with image_path.open("wb") as output_file:
            output_file.write(image.file.read())

        image_paths.append(str(image_path))

    results = process_batch(image_paths)

    return {
    "results": [
        {
            "image_path": result.image_path,
            "status": result.status,
            "draft": (
                result.draft.model_dump()
                if result.draft
                else None
            ),
            "draft_path": result.draft_path,
            "error": result.error,
        }
        for result in results
    ]
}