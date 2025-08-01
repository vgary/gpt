from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load resume content once on startup
with open("gary_resume.txt", encoding="utf-8") as f:
    resume_text = f.read()

class ChatInput(BaseModel):
    user_input: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return PlainTextResponse("OK")


@app.post("/chat")
async def chat_endpoint(chat: ChatInput):
    question = chat.user_input.strip()

    prompt = (
        "You are GaryGPT, an AI assistant trained on Gary's resume below.\n\n"
        f"{resume_text}\n\n"
        f"Answer this question concisely and clearly:\n{question}\n"
    )

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5,
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Sorry, something went wrong: {e}"

    return JSONResponse({"response": answer})
