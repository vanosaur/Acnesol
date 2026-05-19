"""
Lightweight TF-IDF RAG — replaces ChromaDB + SentenceTransformers.
Saves ~150-200MB of RAM, critical for Render free tier (512MB limit).
Retrieval quality is equivalent for short domain-specific knowledge bases.
"""
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBase:
    """In-memory TF-IDF knowledge base. Zero heavy model downloads."""

    def __init__(self, filepath: str = "data/acne_knowledge.txt"):
        self.filepath = filepath
        self.chunks = []
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = None
        self._load_and_index()

    def _load_and_index(self):
        try:
            with open(self.filepath, "r") as f:
                text = f.read()
            self.chunks = [c.strip() for c in text.split("\n\n") if c.strip() and len(c.strip()) > 30]
            if self.chunks:
                self.matrix = self.vectorizer.fit_transform(self.chunks)
                print(f"TF-IDF KnowledgeBase: indexed {len(self.chunks)} chunks.")
        except FileNotFoundError:
            print(f"Warning: {self.filepath} not found. RAG disabled.")

    def retrieve(self, query: str, top_k: int = 3) -> list:
        if self.matrix is None or not self.chunks:
            return []
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices if scores[i] > 0]

    def get_info(self) -> dict:
        return {"mode": "tfidf", "num_chunks": len(self.chunks)}


def load_knowledge_base(path: str = "data/acne_knowledge.txt"):
    return KnowledgeBase(path)
