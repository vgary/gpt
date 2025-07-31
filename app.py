from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize chat history with a system message
chat_history = [{"role": "system", "content": "You are GaryGPT, an AI version of Gary Tong."}]

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    global chat_history
    chat_history.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    assistant_reply = response.choices[0].message['content']
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})
