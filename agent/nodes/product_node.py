from agent.state import PipelineState
from tools.search_tool import search_skincare_products

def run_product_node(state: PipelineState) -> PipelineState:
    # Build search query based on severity
    base_severity = state.lifestyle_result or "Mild"
    img_severity = state.image_result or ""
    
    query = f"best current highly rated skincare products for {base_severity} {img_severity} acne"
    
    # Grab 3 products from live web search
    state.recommended_products = search_skincare_products(query, max_results=3)
    return state
