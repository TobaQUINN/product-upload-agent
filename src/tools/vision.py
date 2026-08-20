from pathlib import Path

from PIL import Image

from src.config import client
from src.schemas.product import ProductIdentification

from src.schemas.image import ImageInput
from src.tools.image_loader import load_image


def analyze_product_image(image: ImageInput) -> ProductIdentification:
    image_data = load_image(image)

    prompt = """
You are identifying a product from its packaging or product image.

Extract only information that can be reasonably determined from the image.

Identify:
- Brand
- Product name
- Model number
- Product type
- Important visible text
- Important specifications clearly visible on the packaging/product

Rules:
- Be precise and direct with words, do not populate words unnecessarily e.g 'High performance powerbank' should be just 'PowerBank'
- Do not invent information.
- Do not guess a model number.
- If something is not visible or cannot be determined, use "Unknown".
- Preserve important model numbers and specifications exactly where possible.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[image_data, prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": ProductIdentification,
        },
    )

    return ProductIdentification.model_validate_json(response.text)
