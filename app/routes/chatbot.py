from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

router = APIRouter()

class Message(BaseModel):
    message: str

# Load system prompt (optional)
try:
    with open("app/data/about_dhrub.txt", encoding="utf-8") as f:
        system_prompt = f.read()
except FileNotFoundError:
    system_prompt = "You are a helpful AI assistant for a portfolio chatbot."

@router.post("/talk-to-bot")
async def chat_with_ai(data: Message):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.message}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
        result = response.json()

        if "error" in result:
            return {"reply": f"Error: {result['error']['message']}"}

        return {"reply": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
