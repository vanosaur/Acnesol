from duckduckgo_search import DDGS

def search_skincare_products(query: str, max_results: int = 3) -> list:
    """Searches duckduckgo for top skincare products matching the query."""
    try:
        results = DDGS().text(query, max_results=max_results)
        return [{"title": r["title"], "snippet": r["body"]} for r in results]
    except Exception as e:
        print(f"Web search failed: {e}")
        return []
