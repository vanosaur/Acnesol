import re

with open('app/app.py', 'r') as f:
    text = f.read()

# Mock the execution pipeline if key is "demo"
demo_patch = """
        if st.session_state.groq_key == "demo":
            import time
            time.sleep(2)  # Simulate processing
            pipeline_state = create_state(sleep=sleep, stress=stress, bmi=bmi, image=uploaded_pil)
            pipeline_state.lifestyle_result = "Moderate"
            pipeline_state.image_result = "Mild" if uploaded_pil else None
            pipeline_state.predicted_class = "Papules" if uploaded_pil else "Unknown"
            pipeline_state.final_severity = "Moderate"
            pipeline_state.ai_text = \"\"\"
## Assessment
Based on your lifestyle and inputs, you have a moderate risk profile.

## Likely Causes
- Elevated stress levels
- Inconsistent sleep leading to weakened barrier

## Morning Routine
- Gentle Cleanser
- Vitamin C Serum
- Lightweight Moisturizer
- SPF 50 Sunscreen

## Night Routine
- Double Cleanse
- Salicylic Acid Treatment
- Rich Night Cream

## Lifestyle Advice
- Try meditation to lower stress.
- Aim for 8 hours of sleep.

## Keep Going!
You are doing great, consistency is key!
\"\"\"
        else:
            resources["llm_client"] = Groq(api_key=st.session_state.groq_key)
            pipeline_state = create_state(sleep=sleep, stress=stress, bmi=bmi, image=uploaded_pil)
            history = st.session_state.analysis_history
            pipeline_state = run_pipeline(pipeline_state, resources, history)
"""

# Replace the execution block
text = re.sub(
    r'resources\["llm_client"\] = Groq\(api_key=st\.session_state\.groq_key\)\n\s+st\.session_state\._step = 3\n\n\s+with st\.spinner\("✨ Running AI agent pipeline \(Analyzing, Searching Live Web\)\.\.\."\):\n\s+pipeline_state = create_state\(sleep=sleep, stress=stress, bmi=bmi, image=uploaded_pil\)\n\s+history = st\.session_state\.analysis_history\n\s+pipeline_state = run_pipeline\(pipeline_state, resources, history\)',
    'st.session_state._step = 3\n        with st.spinner("✨ Running AI agent pipeline (Analyzing, Searching Live Web)..."):' + demo_patch,
    text
)

with open('app/app.py', 'w') as f:
    f.write(text)

print("Demo mode injected!")
