# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import openai
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Set your OpenAI key here or use an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatInput(BaseModel):
    user_input: str

# Load Gary's resume once
with open("gary_resume.txt", "r", encoding="utf-8") as file:
    gary_context = file.read()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(chat: ChatInput):
    prompt = f"This is a chatbot that answers questions based on Gary Tong's experience.\nResume:\n{gary_context}\n\nUser: {chat.user_input}\nGaryGPT:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are GaryGPT, an AI chatbot version of Gary Tong."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message["content"].strip()
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
