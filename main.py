from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# --- CORS MIDDLEWARE (Keep this exactly as is) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True, # Add this for better browser compatibility
    allow_methods=["*"],
    allow_headers=["*"],
)

S26_SPECS = """...your specs..."""

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_samsung(request: ChatRequest):
    # GET THE KEY FROM RENDER ENVIRONMENT VARIABLES
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Initialize the client with the real key
    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a premium Samsung AI Sales Assistant. Answer accurately using ONLY: {S26_SPECS}."},
                {"role": "user", "content": request.message}
            ],
            max_tokens=150
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        # This helps you see the real error in Render logs
        print(f"Error: {e}")
        return {"answer": "I'm having trouble connecting to my brain. Please try again later."}
