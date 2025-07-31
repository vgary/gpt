from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load resume ONCE and keep it hidden from user
with open("gary_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

# Global message history with system prompt only once
chat_history = [
    {"role": "system", "content": "You are GaryGPT, an AI assistant that answers questions based on Gary Tong's experience. Use only the resume as context."},
    {"role": "system", "content": resume_text}
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    visible_history = [msg for msg in chat_history if msg["role"] != "system"]
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": visible_history})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    chat_history.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=chat_history
    )
    assistant_reply = response["choices"][0]["message"]["content"]
    chat_history.append({"role": "assistant", "content": assistant_reply})

    visible_history = [msg for msg in chat_history if msg["role"] != "system"]
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": visible_history})
