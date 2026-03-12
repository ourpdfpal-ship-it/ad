from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# 1. ALLOW CROSS-ORIGIN (Critical for Ads)
# This allows your HTML ad unit to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. THE KNOWLEDGE BASE (RAG Lite)
# In a real app, this would be a PDF or Database. 
S26_SPECS = """
Product: Samsung Galaxy S26 Ultra (Released Feb 2026)
Display: 6.9-inch Dynamic AMOLED 2X, 3000 nits peak brightness, 120Hz.
Special Feature: World's first built-in 'Privacy Display' (hardware-level screen shielding).
Camera: 200MP main (f/1.4 aperture - 47% more light), 50MP 5x Periscope, 50MP Ultra-wide, 10MP 3x Telephoto.
Video: 8K 30fps, 4K 120fps, 360-degree Horizontal Lock stabilization.
Processor: Snapdragon 8 Elite Gen 5 for Galaxy.
Battery: 5000mAh, 60W Wired Super Fast Charging.
Colors: Cobalt Violet, Sky Blue, Black, White.
Price: Starts at $1,299.
"""

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_samsung(request: ChatRequest):
    # Setup your OpenAI Key (Set this in your Hosting Environment Secrets)
    client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a premium Samsung AI Sales Assistant. Answer questions accurately using ONLY this data: {S26_SPECS}. Be concise and helpful."},
            {"role": "user", "content": request.message}
        ],
        max_tokens=150
    )
    
    return {"answer": response.choices[0].message.content}