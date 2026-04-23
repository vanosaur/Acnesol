from agent.state import PipelineState
from tools.rag_tool import KnowledgeBase

def run_rag_node(state: PipelineState, kb: KnowledgeBase) -> PipelineState:
    # Combine final inferred state into a query
    base_severity = state.lifestyle_result
    img_severity = state.image_result or ""
    img_class = state.predicted_class or ""
    
    query = f"acne {base_severity} {img_severity} {img_class} severity duration {state.duration} pain {state.pain_level} worsening {state.worsening}"
    state.rag_chunks = kb.retrieve(query, top_k=4)
    return state
