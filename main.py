from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Data
with open('schemes.json', 'r', encoding='utf-8') as f:
    schemes_data = json.load(f)

# TF-IDF Model Setup
descriptions = [scheme['description'] + " " + scheme['eligibility'] for scheme in schemes_data]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(descriptions)

@app.get("/search")
def search_scheme(query: str):
    # Process Query
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    best_match_idx = similarities.argmax()
    best_score = similarities[best_match_idx]

    if best_score > 0.1: # Threshold
        best_scheme = schemes_data[best_match_idx]
        return {
            "best_scheme": best_scheme,
            "match_score": round(float(best_score), 2)
        }
    else:
        return {"message": "Maaf karein, isse judi koi scheme nahi mili. Thoda aur detail mein likhein."}
