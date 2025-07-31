from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Read the resume file once at startup
with open("gary_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize chat history with system prompt including resume text
chat_history = [
    {"role": "system", "content": (
        "You are GaryGPT, an AI version of Gary Tong. Answer questions based on Gary's professional background."
        f"\n\n{resume_text}"
    )}
]

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    global chat_history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    assistant_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return RedirectResponse(url="/", status_code=303)
