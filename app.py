from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Global chat history starting with system prompt
chat_history = [{"role": "system", "content": "You are GaryGPT, an AI version of Gary Tong."}]

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    global chat_history
    # Append user input to history
    chat_history.append({"role": "user", "content": user_input})

    # Call OpenAI chat completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    assistant_reply = response.choices[0].message.content

    # Append assistant reply to history
    chat_history.append({"role": "assistant", "content": assistant_reply})

    # Redirect to GET / to prevent duplicate submissions on refresh
    return RedirectResponse(url="/", status_code=303)
