from agent.state import PipelineState
def run_guardrail_node(state: PipelineState, client) -> PipelineState:
    from groq import Groq
    # 1. Check if condition is extremely severe
    is_severe = "severe" in str(state.final_severity).lower()
    
    # 2. Add fixed disclaimer logic directly based on exact symptoms
    if is_severe:
        disclaimer = "\n\n> **⚠️ MEDICAL ALERT:** Your analysis indicates severe acne. The AI routine above is for general guidance only. You MUST consult a board-certified dermatologist for prescription treatments like oral antibiotics or isotretinoin to avoid permanent scarring."
        state.ai_text = state.ai_text + disclaimer
        state.is_safe = False # Marked unsafe for general AI solo handling
        return state

    # 3. Use LLM to verify there's no prescriptive diagnosis
    check_prompt = f"""
Review the following skincare advice. Does it contain illegal medical diagnostic phrases like "You have a bacterial infection" or prescriptive drug advice like "Take 2 pills of Accutane"?
Reply ONLY with "SAFE" or "UNSAFE".
Advice:
{state.ai_text}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": check_prompt}]
        )
        safety_result = response.choices[0].message.content.strip().upper()
        
        if "UNSAFE" in safety_result:
            state.is_safe = False
            state.ai_text += "\n\n> **⚠️ NOTE:** Portions of this advice may sound prescriptive. Please remember this is AI-generated and not medical doctrine. Consult a doctor for real diagnosis."
    except Exception:
        pass # If check fails, fail open but safe
        
    return state
