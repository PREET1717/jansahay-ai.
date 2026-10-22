from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Teri API Key set ho gayi hai
genai.configure(api_key="AQ.Ab8RN6J8VXDHFkVyEY2W2dAzRZHEm2IRpY27fl0DXPJS1kPS2A")
model = genai.GenerativeModel('gemini-1.5-flash')

# Load Data
try:
    with open('schemes.json', 'r', encoding='utf-8') as f:
        schemes_data = json.dumps(json.load(f))
except:
    schemes_data = "No local data."

@app.get("/search")
def search_scheme(query: str):
    # AI ko sikhane ke liye prompt
    prompt = f"""
    Tu ek bhartiya sarkari scheme assistant hai jiska naam 'JanSahay AI' hai. 
    Tere paas ye schemes ki jankari hai: {schemes_data}.
    Agar user 'hi', 'hello' bole, toh pyaar se Hindi/Hinglish mein baat kar.
    Agar user kisi scheme ke baare mein puche, toh upar diye data se jawab de, aur agar wahan na ho toh apni knowledge se short mein ekdum badiya jawab de.
    User ka sawal: {query}
    """
    
    try:
        response = model.generate_content(prompt)
        ai_reply = response.text
        
        # Frontend ke design me fit baithne ke liye format
        return {
            "best_scheme": {
                "name": "JanSahay AI Jawab:",
                "description": ai_reply,
                "eligibility": "Sabhi ke liye"
            },
            "match_score": 100
        }
    except Exception as e:
        return {"message": "Server abhi busy hai, 1 minute baad try karein."}
