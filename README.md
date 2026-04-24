# 🌟 AcneSol: Intelligent AI Dermatology Assistant

**AcneSol** is a full-stack, AI-powered skincare consultation platform designed to provide professional-grade dermatology insights from the comfort of home. By combining computer vision (TensorFlow) with advanced LLM reasoning (Groq/Llama 3), AcneSol analyzes skin conditions and lifestyle factors to generate highly personalized skincare routines.

---

## ✨ Key Features

- **📸 Dual-Stream Analysis**: Combines high-accuracy image classification (MobileNetV2) with a clinical-style lifestyle consultation.
- **🧠 Personalized Routines**: Generates unique Morning and Night routines tailored specifically to the user's acne type (Blackheads, Pustules, Cysts, etc.) and severity level.
- **🔍 RAG-Powered Insights**: Uses Retrieval Augmented Generation (RAG) to pull evidence-based advice from a curated dermatology knowledge base.
- **💬 AI Chat Assistant**: After analysis, users can chat with "AcneSol" to ask follow-up questions about their routine or specific ingredients.
- **🎨 Premium UI/UX**: A modern, glassmorphic React interface featuring smooth animations (Framer Motion) and a responsive multi-step consultation flow.

---

## 🛠 Tech Stack

### Backend (The Brain)
- **FastAPI**: High-performance Python web framework.
- **TensorFlow (CPU)**: Custom-trained MobileNetV2 for localized skin condition detection.
- **Groq SDK**: Ultra-fast inference using Llama 3.3 for personalized consultation text.
- **Scikit-Learn (TF-IDF)**: Memory-efficient RAG implementation optimized for low-resource environments (Render Free Tier).

### Frontend (The Face)
- **React 18 + Vite**: Lightning-fast frontend development and build.
- **Tailwind CSS**: Modern utility-first styling.
- **Framer Motion**: Fluid UI transitions and micro-animations.
- **Lucide React**: Beautiful, consistent iconography.

---

## 🚀 Deployment & Infrastructure

AcneSol is built with a **decoupled architecture** for maximum stability:

- **Backend**: Hosted on **Render** (Python 3.10). Optimized with a "Weights-Only" loading strategy to bypass Keras version conflicts and fit within the 512MB RAM limit.
- **Frontend**: Hosted on **Vercel**. Communicates with the Render API via dynamic environment variables.

---

## 💻 Local Setup

### Backend
1. Navigate to the root directory.
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your `GROQ_API_KEY` to a `.env` file.
5. Start the server: `uvicorn api.main:app --reload`

### Frontend
1. Navigate to `cd frontend`.
2. Install dependencies: `npm install`
3. Create a `.env` file and set `VITE_API_URL=http://localhost:8000`.
4. Start the dev server: `npm run dev`

---

## ⚠️ Medical Disclaimer

*AcneSol is an AI-powered educational tool and does not provide medical diagnoses. Always consult with a board-certified dermatologist for persistent or severe skin conditions. The routines provided are for informational purposes only.*

---

<p align="center">
  Built with ❤️ by the me!
</p>
