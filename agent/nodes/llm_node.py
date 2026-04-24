from agent.state import PipelineState

def run_llm_node(state: PipelineState, client, analysis_history: list = None) -> PipelineState:
    from groq import Groq
    # Build image info string
    if state.image_result and state.image_result != "Uncertain":
        img_info = f"{state.predicted_class} ({state.image_result}, confidence: {state.confidence_label})"
    elif state.image_result == "Uncertain":
        img_info = f"{state.predicted_class} (confidence too low to determine severity)"
    else:
        img_info = "No image provided"

    rag_context = "\n\n".join(state.rag_chunks) if state.rag_chunks else "General acne care knowledge."

    products_context = ""
    if state.recommended_products:
        products_context = "### Referenced Products:\n"
        for p in state.recommended_products:
            products_context += f"- **{p['title']}**: {p['snippet']}\n"
        products_context += "\n"

    # Build consultation summary
    consultation = f"""
User Consultation Answers:
- Breakout duration: {state.duration}
- Getting worse: {state.worsening}
- Pain level: {state.pain_level}
- Uses skincare products: {state.skincare_routine}
- Started new products recently: {state.new_products}
- Recent stress increase: {state.stress_change}
- Recent sleep change: {state.sleep_change}
"""

    prompt = f"""You are a friendly dermatologist assistant named AcneSol.
Your goal is to provide a personalized skincare routine based on a user's image analysis and consultation answers.

Reference knowledge:
{rag_context}
{products_context}

IMAGE & LIFESTYLE PROFILE:
- Condition Detected: {img_info}
- FINAL SEVERITY ASSESSMENT: {state.lifestyle_result}
- Identified Primary Trigger: {state.main_trigger}

USER CONSULTATION SUMMARY:
{consultation}

STRICT ADVICE GUIDELINES BASED ON SEVERITY ({state.lifestyle_result}):
1. MILD: Focus on gentle cleansing, non-comedogenic hydration, and preventive care. Suggest one mild active like 2% Salicylic Acid or Niacinamide.
2. MODERATE: Focus on targeted treatment of active lesions. Suggest stronger actives like Benzoyl Peroxide or Adapalene (mention starting slowly). Emphasize barrier repair.
3. SEVERE: Prioritize inflammation reduction and avoiding scarring. Recommend extremely gentle, fragrance-free products. Your primary advice must be a dermatologist consultation for prescription care.

STRICT TONE & FORMAT INSTRUCTIONS:
- Tone: Calm, supportive, and non-medical. Use "may benefit from" instead of "will cure".
- Routine Personalization: Adjust the step complexity based on their current routine and pain level.
- Format: You MUST respond in EXACTLY this format:

💖 Skin Summary:
(1–2 lines: assessment of the {state.lifestyle_result} condition + how the trigger {state.main_trigger} might be involved.)

🔍 Main Insight:
(✨ Focus: {state.main_trigger}. One sentence on why this is the likely driver of current breakouts.)

🧠 What we considered:
- Image: {state.predicted_class} ({state.image_result})
- Adjusted Severity: {state.lifestyle_result}
- Key Factors: {state.duration}, pain: {state.pain_level}, stress: {state.stress_change}

🌞 Morning Routine:
- (step 1: Cleanse)
- (step 2: Targeted Treatment or Hydration)
- (step 3: SPF - mandatory)

🌙 Night Routine:
- (step 1: Cleanse)
- (step 2: Treatment based on {state.lifestyle_result})
- (step 3: Moisturize)

🧴 Product Guidance:
- (Ingredient 1) -> (Benefit for {state.lifestyle_result} acne)
- (Ingredient 2) -> (Benefit)
- (Ingredient 3) -> (Benefit)

🌿 Lifestyle Tip:
(1 personalized suggestion based on: {state.main_trigger})

⚠️ Note:
(1–2 sentences: AI disclaimer + specific level of urgency for a dermatologist visit based on severity: {state.lifestyle_result})
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=900
    )

    state.ai_text = response.choices[0].message.content
    return state
