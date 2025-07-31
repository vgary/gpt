from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory conversation history
conversation_history: List[dict] = [
    {
        "role": "system",
        "content": "You are GaryGPT, an AI version of Gary Tong. You help people understand Gary's experience, skills, values, and accomplishments. Answer like you're helpful and knowledgeable, with a friendly tone."
    }
]

# Request model
class Question(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(question: Question):
    user_input = question.question
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # You can change to gpt-3.5-turbo if needed
            messages=conversation_history,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": reply})

        return {"answer": reply}

    except Exception as e:
        error_message = f"Error: {str(e)}"
        conversation_history.append({"role": "assistant", "content": error_message})
        return {"answer": error_message}
