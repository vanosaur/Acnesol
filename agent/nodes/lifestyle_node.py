from agent.state import PipelineState

SEVERITY_LEVELS = ["Mild", "Moderate", "Severe"]

def _escalate(severity: str, worsening: str, pain: str) -> str:
    """Refined escalation logic based on clinical signals."""
    if severity not in SEVERITY_LEVELS:
        return severity # e.g. "Uncertain"
        
    idx = SEVERITY_LEVELS.index(severity)
    
    # HIGHEST PRIORITY: Inflammatory Flare (+1 Level)
    if worsening == "Yes" and pain == "Painful / deep":
        new_idx = min(idx + 1, len(SEVERITY_LEVELS) - 1)
        return SEVERITY_LEVELS[new_idx]
        
    # BORDERLINE: Leaning state
    if severity == "Moderate" and (worsening == "Yes" or pain == "Painful / deep"):
        return "Moderate (leaning toward severe)"
        
    return severity

def _get_trigger(state: PipelineState) -> str:
    """Return single prioritized trigger."""
    if state.new_products == "Yes":
        return "New Product Reaction"
    if state.worsening == "Yes" and state.pain_level == "Painful / deep":
        return "Progressive inflammatory acne flare"
    if state.worsening == "Yes":
        return "Progressive acne flare"
    if state.stress_change == "Yes":
        return "Stress-related trigger"
    return "General acne factors"

def run_lifestyle_node(state: PipelineState, model) -> PipelineState:
    # Start from image model severity as primary signal
    base_severity = state.image_result or "Mild"

    # Apply refined escalation
    adjusted = _escalate(base_severity, state.worsening, state.pain_level)

    state.lifestyle_result = adjusted
    state.main_trigger = _get_trigger(state)
    return state

