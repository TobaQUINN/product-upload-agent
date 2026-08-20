from dataclasses import dataclass
from pathlib import Path

from google.genai.errors import ClientError

from src.ai_agent.agent import run_product_agent
from src.schemas.image import ImageInput
from src.schemas.product import ProductDraft

@dataclass
class BatchResult:
    image_path: str
    status: str
    draft_path: str | None = None
    draft: ProductDraft | None = None
    error: str | None = None

def process_batch(image_paths: list[str]) -> list[BatchResult]:
    """
    Process product images one at a time.

    Each image is handled independently so one failure
    does not automatically destroy the entire batch.
    """

    results = []

    for image_path in image_paths:
        print("\n" + "=" * 70)
        print(f"PROCESSING: {image_path}")
        print("=" * 70)

        try:
            image = ImageInput(source="local", identifier=image_path)
            draft = run_product_agent(image)

            output_path = Path("output") / f"{Path(image_path).stem}.json"

            results.append(
                BatchResult(
                    image_path=image_path,
                    status="completed",
                    draft_path=str(output_path),
                    draft=draft
                )
            )

        except ClientError as error:
            error_message = str(error)

            if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                print("\nGemini quota exceeded.")
                print("Stopping batch to avoid unnecessary requests.")

                results.append(
                    BatchResult(
                        image_path=image_path,
                        status="quota_exceeded",
                        error="Gemini API quota exceeded.",
                    )
                )

                # Stop because subsequent images will hit the same quota.
                break

            results.append(
                BatchResult(
                    image_path=image_path,
                    status="api_error",
                    error=error_message,
                )
            )

        except (ConnectionError, TimeoutError) as error:
            results.append(
                BatchResult(
                    image_path=image_path,
                    status="network_error",
                    error=str(error),
                )
            )

        except FileNotFoundError as error:
            results.append(
                BatchResult(
                    image_path=image_path,
                    status="image_not_found",
                    error=str(error),
                )
            )

        except Exception as error:
            results.append(
                BatchResult(
                    image_path=image_path,
                    status="failed",
                    error=str(error),
                )
            )

    return results
