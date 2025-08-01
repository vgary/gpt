from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os

# Load resume content once at startup
with open("gary_resume.txt", "r") as f:
    resume_text = f.read()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chat_history = []

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    prompt = f"""You are a helpful AI assistant who knows everything about Gary based on his resume below.

Resume:
{resume_text}

Conversation history:
{format_chat_history(chat_history)}

User: {user_input}
AI:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        assistant_response = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        assistant_response = f"Error: {e}"

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": assistant_response})

    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_history": chat_history
    })

def format_chat_history(history):
    result = ""
    for msg in history:
        result += f"{msg['role'].capitalize()}: {msg['content']}\n"
    return result
