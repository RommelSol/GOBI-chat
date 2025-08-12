import os, re, math
from dataclasses import dataclass
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .document_reader import load_text_from_path
from .config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, MAX_WORDS

@dataclass
class Chunk:
    text: str
    source: str   # ruta del archivo
    meta: Dict[str, Any]

def _chunk_text(s: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[str]:
    s = re.sub(r"\s+", " ", s).strip()
    if not s: return []
    chunks, i = [], 0
    while i < len(s):
        chunks.append(s[i:i+size])
        i += (size - overlap)
    return chunks

def build_index(paths: List[str]):
    chunks: List[Chunk] = []
    for p in paths:
        try:
            txt = load_text_from_path(p)
        except Exception as e:
            print(f"[WARN] No pude leer {p}: {e}")
            continue
        for idx, c in enumerate(_chunk_text(txt)):
            chunks.append(Chunk(text=c, source=p, meta={"chunk_id": idx}))
    corpus = [c.text for c in chunks] if chunks else [""]
    vectorizer = TfidfVectorizer(strip_accents="unicode", ngram_range=(1,2), max_df=0.9, min_df=1)
    X = vectorizer.fit_transform(corpus)
    return {"vectorizer": vectorizer, "matrix": X, "chunks": chunks}

def infer_paths_from_dir(root=DOCS_DIR) -> List[str]:
    if not os.path.isdir(root): return []
    out = []
    for f in os.listdir(root):
        if f.lower().endswith((".pdf", ".docx", ".doc")):
            out.append(os.path.join(root, f))
    return sorted(out)

def retrieve(query: str, index, k=TOP_K) -> List[Chunk]:
    if not index["chunks"]: return []
    vec = index["vectorizer"].transform([query])
    sims = cosine_similarity(vec, index["matrix"]).ravel()
    top_idx = sims.argsort()[::-1][:k]
    return [index["chunks"][i] for i in top_idx]

def compose_answer(query: str, hits: List[Chunk]) -> Dict[str, Any]:
    # concatenamos los mejores fragmentos y respetamos el límite
    combined = " ".join([h.text for h in hits]).strip()
    words = combined.split()
    short = " ".join(words[:MAX_WORDS])
    sources = list({(os.path.basename(h.source), h.source) for h in hits})
    return {
        "answer": short + ("..." if len(words) > MAX_WORDS else ""),
        "sources": [{"name": n, "path": p} for (n, p) in sources]
    }