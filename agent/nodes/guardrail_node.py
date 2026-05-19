import re
from agent.state import PipelineState

# Regex-based patterns that are dangerous/prescriptive — no LLM call needed
_UNSAFE_PATTERNS = re.compile(
    r"\b(you have a bacterial infection|take \d+ pill|prescrib|isotretinoin dosage|oral antibiotic dose|i diagnose|medical diagnosis)\b",
    re.IGNORECASE
)

def run_guardrail_node(state: PipelineState, client) -> PipelineState:
    # 1. Check if condition is extremely severe — instant rule check
    is_severe = "severe" in str(state.final_severity).lower()

    if is_severe:
        disclaimer = "\n\n> **⚠️ MEDICAL ALERT:** Your analysis indicates severe acne. The AI routine above is for general guidance only. You MUST consult a board-certified dermatologist for prescription treatments like oral antibiotics or isotretinoin to avoid permanent scarring."
        state.ai_text = state.ai_text + disclaimer
        state.is_safe = False
        return state

    # 2. Fast regex scan — replaces the expensive second LLM API call
    if _UNSAFE_PATTERNS.search(state.ai_text or ""):
        state.is_safe = False
        state.ai_text += "\n\n> **⚠️ NOTE:** Portions of this advice may sound prescriptive. Please remember this is AI-generated and not a medical diagnosis. Consult a doctor for real diagnosis."
    else:
        state.is_safe = True

    return state
