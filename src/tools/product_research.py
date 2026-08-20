from src.config import client
from src.schemas.product import ProductDraft, ProductIdentification


def generate_product_draft(
    identification: ProductIdentification,
    search_results: list[dict],
    image_path: str | None = None,
) -> ProductDraft:
    """
    Generate a product listing draft using the product image analysis
    and web research results.
    """

    research_text = "\n\n".join(
        [
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['snippet']}"
            for result in search_results
        ]
    )

    prompt = f"""
You are a product research assistant for an electronics retail store.

Your task is to create a product listing draft from the available evidence.

PRODUCT IDENTIFICATION FROM IMAGE:
Brand: {identification.brand}
Product Name: {identification.product_name}
Model Number: {identification.model_number}
Product Type: {identification.product_type}
Color/Variant: {identification.color_variant}

VISIBLE TEXT:
{identification.visible_text}

VISIBLE SPECIFICATIONS:
{identification.visible_specifications}

WEB RESEARCH:
{research_text}

Create the following:

1. Product Name
2. Short Description
3. Full Description

DESCRIPTION REQUIREMENTS:

The descriptions must be suitable for an actual online retail product listing.

PRODUCT NAME:
- Give the product a clear, specific name.
- Include the brand and model number when they are verified.
- Include important verified specifications in the name when useful.
- Do not unnecessarily make the product name excessively long.

SHORT DESCRIPTION:
- Keep it concise.
- Summarize what the product is and its most important characteristics.
- Prioritize useful, verified information.
- Avoid prices, warranties, guarantees, and seller-specific claims.

FULL DESCRIPTION:
Choose the most appropriate format based on the amount and complexity of verified product information.

For SIMPLE PRODUCTS:
Use a natural, concise paragraph describing what the product is, what it does,
and its important characteristics.

For PRODUCTS WITH MULTIPLE MEANINGFUL FEATURES OR SPECIFICATIONS:
Use a short introductory paragraph followed by a "Key Features" section.

Format the Key Features section like this:

Key Features

Feature: Explanation of what the feature is and what it means for the customer.

Feature: Explanation of what the feature is and what it means for the customer.

Feature: Explanation of what the feature is and what it means for the customer.

Each feature must explain the practical meaning or benefit of the feature.
Do not merely list specifications without explaining them.

For example:

22.5W Fast Charging: Provides faster charging for compatible devices,
helping reduce the time required to recharge them.

50,000mAh Capacity: Provides a large power reserve for charging compatible
devices multiple times before the power bank itself needs to be recharged.

IMPORTANT:
- Do not force a Key Features section onto simple products.
- Do not create features simply to make the description longer.
- Only include features and specifications supported by the image or credible
  research evidence.
- Do not combine specifications from different models.
- Do not assume that a specification belongs to this product simply because
  it appears on a page about the same brand.
- Prefer manufacturer information when available.
- Do not include public prices.
- Do not include company warranties or guarantees.
- Do not include seller-specific claims.
- Do not invent specifications.
- Do not exaggerate product capabilities.
- Do not make unsupported marketing claims.
- Do not mention the research process in the descriptions.
- If information cannot be verified, leave it out rather than guessing.

BUSINESS-SPECIFIC FIELDS:

The following fields must NOT be decided by you:

- Category
- Price
- Stock quantity
- Availability
- Featured

Leave those fields empty.

Return the result using the ProductDraft schema.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ProductDraft,
        },
    )

    draft = ProductDraft.model_validate_json(response.text)

    if image_path:
        draft.image_path = image_path

    return draft
