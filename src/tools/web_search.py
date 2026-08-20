from ddgs import DDGS
from src.schemas.product import ProductIdentification


def build_search_query(product: ProductIdentification) -> str:
    """
    Build a precise web search query from the product identification.
    """

    query_parts = [
        product.brand,
        product.model_number,
        product.product_type,
    ]

    return " ".join(
        part for part in query_parts
        if part and part.lower() != "unknown"
    )


def search_product(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web for information about a product.
    """

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=max_results,
        )

        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", ""),
            })

    return results
