from duckduckgo_search import DDGS

# Curated fallback products by severity — shown if web search fails/times out
_FALLBACK_PRODUCTS = {
    "mild": [
        {"title": "CeraVe Foaming Facial Cleanser", "snippet": "A gentle, non-comedogenic cleanser with ceramides and niacinamide. Great for mild acne-prone skin."},
        {"title": "The Ordinary Niacinamide 10% + Zinc 1%", "snippet": "Reduces blemishes and pore appearance. Clinically proven for mild to moderate acne."},
        {"title": "Neutrogena Oil-Free Acne Moisturizer SPF 35", "snippet": "Non-greasy, oil-free moisturizer with SPF. Ideal for daily acne-prone skin protection."},
    ],
    "moderate": [
        {"title": "Paula's Choice 2% BHA Liquid Exfoliant", "snippet": "Salicylic acid exfoliant that unclogs pores deeply. Highly rated for moderate acne and blackheads."},
        {"title": "La Roche-Posay Effaclar Duo", "snippet": "Targets persistent moderate acne with benzoyl peroxide and LHA. Reduces breakouts and marks."},
        {"title": "CeraVe AM Facial Moisturizing Lotion SPF 30", "snippet": "Lightweight ceramide-rich SPF moisturizer. Repairs the skin barrier while protecting from sun damage."},
    ],
    "severe": [
        {"title": "La Roche-Posay Effaclar K+ Serum", "snippet": "Targets severe oil and clogged pores. Dermatologist-recommended for severe acne-prone skin."},
        {"title": "Differin Adapalene Gel 0.1%", "snippet": "OTC retinoid for severe acne. Clinically proven to reduce cystic breakouts over time."},
        {"title": "CeraVe Moisturizing Cream", "snippet": "Rich barrier repair cream. Essential for severe acne skin undergoing active treatment."},
    ],
    "default": [
        {"title": "CeraVe Hydrating Cleanser", "snippet": "Gentle hydrating cleanser suitable for all skin types. Maintains the skin's natural moisture barrier."},
        {"title": "The Ordinary Salicylic Acid 2% Solution", "snippet": "Targets acne-causing congestion. Lightweight formula safe for daily use on blemish-prone skin."},
        {"title": "EltaMD UV Clear Broad-Spectrum SPF 46", "snippet": "Dermatologist-recommended SPF for acne-prone and sensitive skin. Oil-free, lightweight, and non-comedogenic."},
    ]
}

def _get_fallback(severity: str) -> list:
    """Return curated fallback products based on severity."""
    key = severity.lower() if severity else "default"
    for k in ["severe", "moderate", "mild"]:
        if k in key:
            return _FALLBACK_PRODUCTS[k]
    return _FALLBACK_PRODUCTS["default"]

def search_skincare_products(query: str, max_results: int = 3, severity: str = "") -> list:
    """Searches duckduckgo for top skincare products matching the query.
    Falls back to curated product list if search fails or times out.
    """
    try:
        results = DDGS().text(query, max_results=max_results, timeout=3)
        if results:
            return [{"title": r["title"], "snippet": r["body"]} for r in results]
        # Empty results — serve fallback
        return _get_fallback(severity)
    except Exception as e:
        print(f"Web search failed or timed out: {e}. Serving curated fallback products.")
        return _get_fallback(severity)
