import os
from dotenv import load_dotenv

load_dotenv()
import io
import base64
from fastapi import FastAPI, UploadFile, Form, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from PIL import Image

# Import agent and tools
from agent.graph import create_state, run_pipeline


app = FastAPI(title="AcneSol API Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "AcneSol API"}

# Global resources dictionary cache
resources_cache = {
    "ml_model": None,
    "cnn_model": None,
    "knowledge_base": None,
}

def get_resources():
    # Lazy load heavy resources to avoid blocking startup
    from tools.ml_tool import load_ml_model
    from tools.image_tool import load_cnn_model
    from tools.rag_tool import load_knowledge_base
    
    if resources_cache["knowledge_base"] is None:
        try: resources_cache["knowledge_base"] = load_knowledge_base("data/acne_knowledge.txt")
        except: pass
    if resources_cache["ml_model"] is None:
        try: resources_cache["ml_model"] = load_ml_model()
        except: pass
    if resources_cache["cnn_model"] is None:
        try: resources_cache["cnn_model"] = load_cnn_model()
        except: pass
    return resources_cache

@app.on_event("startup")
async def startup_event():
    # Start pre-warming resources in a background thread so it doesn't block port binding
    import threading
    threading.Thread(target=get_resources, daemon=True).start()


class AnalyzeParams(BaseModel):
    duration: str = ""
    worsening: str = ""
    pain_level: str = ""
    skincare_routine: str = ""
    new_products: str = ""
    stress_change: str = ""
    sleep_change: str = ""
    image_base64: Optional[str] = None
    groq_api_key: Optional[str] = None
    manual_type_override: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatParams(BaseModel):
    message: str
    history: List[ChatMessage] = []
    groq_api_key: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None

@app.post("/api/analyze")
async def analyze_skin(params: AnalyzeParams):
    api_key = params.groq_api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="Groq API Key is required (provide in request or backend .env)")
    
    try:
        from groq import Groq
        llm_client = Groq(api_key=api_key)
    except ImportError as e:
        print(f"CORTEX_DEBUG: ImportError for groq: {e}")
        raise HTTPException(status_code=500, detail=f"Backend dependency error (groq): {e}")
    except Exception as e:
        print(f"CORTEX_DEBUG: Groq init error: {e}")
        raise HTTPException(status_code=401, detail="Invalid Groq API Key")

    resources = get_resources()
    resources["llm_client"] = llm_client

    image = None
    if params.image_base64:
        try:
            img_data = base64.b64decode(params.image_base64.split(",")[1] if "," in params.image_base64 else params.image_base64)
            image = Image.open(io.BytesIO(img_data)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid Base64 Image")

    try:
        state = create_state(
            duration=params.duration,
            worsening=params.worsening,
            pain_level=params.pain_level,
            skincare_routine=params.skincare_routine,
            new_products=params.new_products,
            stress_change=params.stress_change,
            sleep_change=params.sleep_change,
            image=image,
            image_base64=params.image_base64,
            manual_type_override=params.manual_type_override
        )
        
        # run pipeline
        final_state = run_pipeline(state, resources, analysis_history=[])
        
        products_str = "\n".join([f"- {p['title']}" for p in final_state.recommended_products]) if getattr(final_state, 'recommended_products', None) else ""
        return {
            "success": True,
            "lifestyle": getattr(final_state, 'lifestyle_result', "N/A"),
            "image_severity": getattr(final_state, 'image_result', "N/A"),
            "predicted_class": getattr(final_state, 'predicted_class', "N/A"),
            "all_predictions": getattr(final_state, 'all_predictions', {}),
            "confidence_label": getattr(final_state, 'confidence_label', "N/A"),
            "main_trigger": getattr(final_state, 'main_trigger', "N/A"),
            "products": products_str,
            "final": getattr(final_state, 'ai_text', "Analysis complete."),
            "duration": final_state.duration,
            "worsening": final_state.worsening,
            "pain_level": final_state.pain_level,
            "new_products": final_state.new_products,
            "stress_change": final_state.stress_change
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(params: ChatParams):
    from groq import Groq
    api_key = params.groq_api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="Groq API Key is required (provide in request or backend .env)")

    try:
        llm_client = Groq(api_key=api_key)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Groq API Key")

    resources = get_resources()
    kb = resources["knowledge_base"]
    
    # Simple RAG retrieval
    context_chunks = []
    if kb:
        context_chunks = kb.retrieve(params.message, top_k=2)

    context_text = "\n\n".join(context_chunks) if context_chunks else "No specific context retrieved."
    
    profile = ""
    if params.analysis:
        profile = f"""
USER PROFILE (from latest analysis):
- Acne type detected: {params.analysis.get('predicted_class', 'N/A')}
- Image severity: {params.analysis.get('image_severity', 'N/A')}
- Adjusted severity: {params.analysis.get('lifestyle', 'N/A')}
- Model confidence: {params.analysis.get('confidence_label', 'N/A')}
- Main trigger identified: {params.analysis.get('main_trigger', 'N/A')}
- Breakout duration: {params.analysis.get('duration', 'N/A')}
- Getting worse: {params.analysis.get('worsening', 'N/A')}
- Pain level: {params.analysis.get('pain_level', 'N/A')}
- New products used: {params.analysis.get('new_products', 'N/A')}
- Recent stress change: {params.analysis.get('stress_change', 'N/A')}
"""

    system_msg = f"""You are AcneSol, a friendly and knowledgeable AI skincare assistant.
Be warm, concise, and evidence-based. Use the knowledge context below to inform your answers.
If the user has analysis data, reference it to personalize your response.

KNOWLEDGE CONTEXT:
{context_text}
{profile}

Guidelines:
- Keep answers concise (3-6 sentences typically)
- Use bullet points for lists
- Be encouraging and supportive
- Reference the user's specific data when relevant
- If the user needs professional help, suggest seeing a dermatologist
- Never diagnose; you are an AI assistant, not a doctor"""

    messages = [{"role": "system", "content": system_msg}]
    for msg in params.history[-10:]:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": params.message})

    try:
        response = llm_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=600,
        )
        answer = response.choices[0].message.content
        return {"success": True, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
