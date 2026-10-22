from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from sentence_transformers import SentenceTransformer, util
from deep_translator import GoogleTranslator

app = FastAPI(title="JanSahay AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("schemes.json", "r") as f:
    schemes_data = json.load(f)

print("AI Model load ho raha hai, thoda wait kar bhai...")
model = SentenceTransformer('all-MiniLM-L6-v2')

scheme_descriptions = [scheme["description"] for scheme in schemes_data]
scheme_embeddings = model.encode(scheme_descriptions)
print("Model aur Data dono ready hain! Server start ho gaya.")

@app.get("/")
def home():
    return {"status": "success", "message": "JanSahay AI Backend makhan chal raha hai!"}

@app.get("/schemes")
def get_schemes():
    return {"total_schemes": len(schemes_data), "data": schemes_data}

@app.get("/search")
def search_schemes(query: str):
    try:
        translated_query = GoogleTranslator(source='auto', target='en').translate(query)
    except Exception as e:
        print(f"Translation Error: {e}")
        translated_query = query 
        
    query_embedding = model.encode(translated_query)
    results = util.cos_sim(query_embedding, scheme_embeddings)
    
    best_match_index = results.argmax().item()
    best_score = results[0][best_match_index].item()
    
    # Terminal mein check karne ke liye ki AI kya kar raha hai
    print("----- NAYA SEARCH -----")
    print(f"Original: {query}")
    print(f"Translated: {translated_query}")
    print(f"Top Scheme Match Score: {best_score}")
    print("-----------------------")
    
    # Limit ko 0.25 se hata kar 0.15 kar diya hai
    if best_score > 0.15:
        return {
            "query": query,
            "translated_query": translated_query,
            "match_score": round(best_score, 2),
            "best_scheme": schemes_data[best_match_index]
        }
    else:
        return {"message": "Sorry bhai, isse related abhi koi scheme nahi mili."}