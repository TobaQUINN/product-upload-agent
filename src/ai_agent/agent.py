from src.tools.vision import analyze_product_image
from src.tools.web_search import build_search_query, search_product
from src.tools.product_research import generate_product_draft
from src.tools.output_writer import save_product_draft

from src.schemas.image import ImageInput


def run_product_agent(image: ImageInput):
    """
    Run the complete product upload agent workflow.
    """

    print("\n--- ANALYZING PRODUCT IMAGE ---")

    identification = analyze_product_image(image)

    print("\n--- PRODUCT IDENTIFICATION ---")
    print(identification.model_dump_json(indent=2))

    print("\n--- BUILDING SEARCH QUERY ---")

    query = build_search_query(identification)

    print(f"Search query: {query}")

    print("\n--- SEARCHING WEB ---")

    search_results = search_product(query)

    print(f"Found {len(search_results)} search results.")

    print("\n--- GENERATING PRODUCT DRAFT ---")

    draft = generate_product_draft(
        identification=identification,
        search_results=search_results,
        image_path=image.identifier,
    )

    print("\n--- SAVING PRODUCT DRAFT ---")

    output_path = save_product_draft(
        draft=draft,
        image=image,
    )

    print(f"Product draft saved to: {output_path}")

    return draft
