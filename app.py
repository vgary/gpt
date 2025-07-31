from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Set your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")  # Add this to Render as a Secret

client = OpenAI(api_key=openai_api_key)

chat_history = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    global chat_history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_history": chat_history
    })
