import os
# Override HF cache directory to avoid local permission issues on global home folder
os.environ["HF_HOME"] = os.path.abspath("data/hf_cache")

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class KnowledgeBase:
    """Knowledge base using ChromaDB for persistent storage and retrieval."""

    def __init__(self, filepath: str = "data/acne_knowledge.txt", db_path: str = "data/chroma_db"):
        self.filepath = filepath
        self.db_path = db_path
        self.collection_name = "acne_knowledge"
        
        # Initialize persistent client
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Check if collection exists or needs to be created/populated
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            self._is_populated = self.collection.count() > 0
        except:
            self.collection = self.client.create_collection(name=self.collection_name)
            self._is_populated = False

        # Always re-check chunks to see if we need to update
        self._sync_db()

    def _load_chunks(self) -> list:
        try:
            with open(self.filepath, "r") as f:
                text = f.read()
            chunks = [c.strip() for c in text.split("\n\n") if c.strip() and len(c.strip()) > 30]
            return chunks
        except FileNotFoundError:
            print(f"Warning: {self.filepath} not found.")
            return []

    def _sync_db(self):
        chunks = self._load_chunks()
        if not chunks:
            return
            
        current_count = self.collection.count()
        if current_count == len(chunks):
            self._is_populated = True
            return
            
        print("Populating/Updating ChromaDB with knowledge base chunks...")
        # If mismatch in length, just recreate for simplicity in this prototype
        if current_count > 0:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(name=self.collection_name)
            
        embeddings = self.model.encode(chunks, normalize_embeddings=True).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )
        self._is_populated = True
        print(f"Successfully added {len(chunks)} chunks to ChromaDB.")

    def retrieve(self, query: str, top_k: int = 3) -> list:
        if not self._is_populated:
            return []
            
        q_emb = self.model.encode([query], normalize_embeddings=True).tolist()
        results = self.collection.query(
            query_embeddings=q_emb,
            n_results=top_k
        )
        
        if results and results['documents'] and results['documents'][0]:
            return results['documents'][0]
        return []

    def get_info(self) -> dict:
        count = self.collection.count() if self._is_populated else 0
        return {
            "mode": "chromadb",
            "num_chunks": count,
        }

def load_knowledge_base(path: str = "data/acne_knowledge.txt"):
    return KnowledgeBase(path)
