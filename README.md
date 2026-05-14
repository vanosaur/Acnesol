# AcneSol — Your AI-Powered Dermatology Assistant

AcneSol is an intelligent full-stack skincare consultation platform that analyzes facial images and lifestyle factors to generate highly personalized skincare routines. By combining computer vision, retrieval-augmented generation (RAG), and large language models, AcneSol provides evidence-based recommendations tailored to each user's acne type, severity, and daily habits.

## Overview

AcneSol integrates multiple AI components to simulate a structured dermatology consultation.

The system performs the following tasks:

1. Analyzes facial images using a custom-trained MobileNetV2 model.
2. Detects acne type and severity (such as Blackheads, Papules, Pustules, and Cystic Acne).
3. Collects lifestyle information including sleep, stress, diet, and skincare habits.
4. Retrieves evidence-based dermatology knowledge using TF-IDF and cosine similarity.
5. Generates personalized morning and night skincare routines.
6. Recommends suitable ingredients and products.
7. Provides a conversational AI assistant for follow-up questions.
8. Presents all results through a modern and responsive web interface.

The application combines traditional machine learning, deep learning, and generative AI to deliver professional-grade skincare guidance from home.

---

## Features

- Facial image analysis using MobileNetV2 and TensorFlow
- Acne type and severity classification
- Lifestyle-based consultation questionnaire
- Retrieval-augmented generation using TF-IDF
- Personalized morning and night routines
- Ingredient and product recommendations
- Conversational follow-up assistant
- Interactive React-based user interface
- Responsive design with animations and glassmorphism

---

## Technology Stack

### Backend and AI

- Python
- FastAPI
- TensorFlow
- Keras
- MobileNetV2
- Groq SDK
- Llama 3.3 70B
- Scikit-learn
- TF-IDF Vectorizer
- Pillow

### Frontend

- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Lucide React

---

## System Architecture

```text
User Uploads Image and Answers Lifestyle Questions
                        ↓
                  React Frontend
                        ↓
                 FastAPI Backend
                        ↓
           Image Preprocessing (Pillow)
                        ↓
       MobileNetV2 Acne Classification Model
                        ↓
     Lifestyle Response Normalization
                        ↓
    TF-IDF Knowledge Retrieval (RAG)
                        ↓
     Llama 3 Personalized Reasoning
                        ↓
       Structured JSON Response
                        ↓
        Results Dashboard + AI Chat
```

## Core AI Components

### Computer Vision Model

A MobileNetV2 convolutional neural network analyzes uploaded facial images and predicts acne type and severity.

### Retrieval-Augmented Generation

A TF-IDF-based retriever searches a curated dermatology knowledge base for relevant evidence and treatment guidance.

### Large Language Model

Llama 3.3, accessed through the Groq API, combines image predictions, retrieved knowledge, and lifestyle data to generate personalized skincare recommendations.

---

## Personalized Consultation Workflow

1. The user uploads a facial image.
2. The user answers a structured lifestyle questionnaire.
3. The frontend sends all data to the FastAPI backend.
4. The image is resized and normalized using Pillow.
5. MobileNetV2 predicts the acne condition and confidence score.
6. TF-IDF retrieves relevant dermatology content.
7. Llama 3 generates a detailed skincare routine.
8. The backend returns a structured JSON response.
9. The frontend displays routines, recommendations, and supporting explanations.
10. The user can ask follow-up questions through the AI chat assistant.

---

## Deployment

AcneSol uses a decoupled deployment architecture.

- Backend deployed on Render
- Frontend deployed on Vercel
- Environment variables used for API configuration
- Memory-optimized model loading for low-resource hosting

---

## Performance Optimizations

- Lazy loading for frontend pages and components
- Weights-only model loading to reduce RAM usage
- TF-IDF retrieval for lightweight RAG
- Dynamic API URLs using environment variables
- Cached model and retriever initialization

---

## Project Structure

```text
AcneSol/
├── api/                 # FastAPI application and endpoints
├── models/              # Trained MobileNetV2 model files
├── rag/                 # TF-IDF knowledge base and retrieval logic
├── services/            # LLM and recommendation services
├── frontend/            # React application
├── assets/              # Images and static resources
├── requirements.txt     # Python dependencies
└── README.md

```


## Limitations

- The system provides educational guidance, not medical diagnosis.
- Results depend on image quality, lighting, and user responses.
- Recommendations may not replace professional dermatological consultation.

---

## Future Improvements

- Support for additional skin conditions
- Multi-language recommendations
- Progress tracking and routine history
- Ingredient compatibility analysis
- Mobile application support

---

## Medical Disclaimer

AcneSol is an AI-powered educational tool and does not provide medical diagnosis or treatment. Users should consult a qualified dermatologist for persistent or severe skin concerns.

---

## Author

❤️ Built by Vani Rudra.
