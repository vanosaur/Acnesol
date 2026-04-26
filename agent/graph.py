from typing import Dict, Any, Optional
from PIL import Image

from agent.state import PipelineState
from agent.nodes.image_node import run_image_node
from agent.nodes.lifestyle_node import run_lifestyle_node
from agent.nodes.rag_node import run_rag_node
from agent.nodes.product_node import run_product_node
from agent.nodes.llm_node import run_llm_node
from agent.nodes.guardrail_node import run_guardrail_node

def create_state(
    duration: str = "",
    worsening: str = "",
    pain_level: str = "",
    skincare_routine: str = "",
    new_products: str = "",
    stress_change: str = "",
    sleep_change: str = "",
    image: Optional[Image.Image] = None,
    image_base64: Optional[str] = None,
    manual_type_override: Optional[str] = None
) -> PipelineState:
    """Factory to initialize the pipeline state from user inputs."""
    return PipelineState(
        duration=duration,
        worsening=worsening,
        pain_level=pain_level,
        skincare_routine=skincare_routine,
        new_products=new_products,
        stress_change=stress_change,
        sleep_change=sleep_change,
        image=image,
        image_base64=image_base64,
        manual_type_override=manual_type_override
    )

def run_pipeline(state: PipelineState, resources: Dict[str, Any], analysis_history: list = None) -> PipelineState:
    """Orchestrates the pipeline execution."""
    
    # Node 1: Extract image prediction (if available)
    state = run_image_node(state, resources["cnn_model"])
    
    # Node 2: Extract lifestyle prediction (depends on image result)
    state = run_lifestyle_node(state, resources["ml_model"])
    
    # Node 3: Retrieve relevant knowledge
    state = run_rag_node(state, resources["knowledge_base"])
    
    # Node 3.5: Fetch Live Products
    state = run_product_node(state)
    
    # Node 4: Generate insights using LLM
    state = run_llm_node(state, resources["llm_client"], analysis_history)
    
    # Node 5: Medical Guardrail Verification
    state = run_guardrail_node(state, resources["llm_client"])
    
    return state
