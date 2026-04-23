import numpy as np

# Try semantic search first, fall back to TF-IDF
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    _RAG_MODE = "semantic"
except ImportError:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    _RAG_MODE = "tfidf"

class KnowledgeBase:
    """Lightweight knowledge base with semantic or TF-IDF retrieval."""

    def __init__(self, filepath: str = "data/acne_knowledge.txt"):
        self.chunks = self._load_chunks(filepath)
        self.mode = _RAG_MODE
        self._build_index()

    def _load_chunks(self, filepath: str) -> list:
        try:
            with open(filepath, "r") as f:
                text = f.read()
            chunks = [c.strip() for c in text.split("\n\n") if c.strip() and len(c.strip()) > 30]
            return chunks
        except FileNotFoundError:
            return []

    def _build_index(self):
        if not self.chunks:
            return

        if self.mode == "semantic":
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            embeddings = self.model.encode(self.chunks, normalize_embeddings=True)
            self.index = faiss.IndexFlatIP(embeddings.shape[1])
            self.index.add(embeddings.astype("float32"))
        else:
            self.vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=5000,
                ngram_range=(1, 2),
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)

    def retrieve(self, query: str, top_k: int = 3) -> list:
        if not self.chunks:
            return []
        top_k = min(top_k, len(self.chunks))

        if self.mode == "semantic":
            q_emb = self.model.encode([query], normalize_embeddings=True).astype("float32")
            scores, indices = self.index.search(q_emb, top_k)
            return [self.chunks[i] for i in indices[0] if 0 <= i < len(self.chunks)]
        else:
            q_vec = self.vectorizer.transform([query])
            sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
            top_indices = sims.argsort()[-top_k:][::-1]
            return [self.chunks[i] for i in top_indices if sims[i] > 0.02]

    def get_info(self) -> dict:
        return {
            "mode": self.mode,
            "num_chunks": len(self.chunks),
        }

def load_knowledge_base(path: str = "data/acne_knowledge.txt"):
    return KnowledgeBase(path)
