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

Reference knowledge:
{rag_context}
{products_context}

Image Analysis:
- Detected: {img_info}
- Lifestyle impact severity: {state.lifestyle_result}
- Main trigger identified: {state.main_trigger}
{consultation}

STRICT INSTRUCTIONS:
- Tone: Calm, friendly, and non-medical. Avoid absolute certainty; use phrases like "This may be influenced by..." instead of "This is caused by...".
- Specificity: Be specific to THIS user based on their consultation answers and the acne type detected.
- Routine Personalization:
    - If inflammatory acne (Pustules/Cysts) is detected: mention using a gentle salicylic acid cleanser and explicitly advise against harsh scrubbing.
    - If pain is present: suggest extremely gentle care and avoiding any physical irritation.
- Product Guidance: Return ONLY a simplified, ingredient-focused list (e.g., "Salicylic acid -> helps unclog pores"). Do NOT create separate cleanser/treatment categories.
- Do NOT add any extra paragraphs or sections outside the format below.

You MUST respond in EXACTLY this format:

💖 Skin Summary:
(1–2 lines: calm, non-prescriptive assessment of the image + answers)

🔍 Main Insight:
(✨ Main Trigger: {state.main_trigger}. Followed by ONE sentence explaining how this factor may be influencing the skin.)

🧠 What we considered:
- Image analysis: {state.predicted_class or 'N/A'} ({state.image_result or 'N/A'})
- Pattern: {state.duration}, worsening: {state.worsening}
- Lifestyle: stress change: {state.stress_change}, sleep change: {state.sleep_change}
- Skincare: products: {state.skincare_routine}, new products: {state.new_products}

🌞 Morning Routine:
- (step 1)
- (step 2)
- (step 3)

🌙 Night Routine:
- (step 1)
- (step 2)
- (step 3)

🧴 Product Guidance:
- (Ingredient 1) -> (Benefit)
- (Ingredient 2) -> (Benefit)
- (Ingredient 3) -> (Benefit)

🌿 Lifestyle Tip:
(1 personalized, actionable suggestion based on their trigger: {state.main_trigger})

⚠️ Note:
(1–2 sentences: AI disclaimer + recommendation to see a dermatologist for persistent or severe cases)
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=900
    )

    state.ai_text = response.choices[0].message.content
    return state
