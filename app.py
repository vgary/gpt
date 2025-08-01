from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (like index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ GET route for UptimeRobot or health check
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head><title>GaryGPT</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 10%;">
            <h1>GaryGPT is running ✅</h1>
            <p>Ask questions at <a href="/chat">/chat</a> (POST only)</p>
        </body>
    </html>
    """

# 🧠 Model for user input
class MessageInput(BaseModel):
    message: str

# 🎯 POST route for chatbot
@app.post("/chat")
async def chat(input: MessageInput):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that knows everything about Gary Tong's career."},
                {"role": "user", "content": input.message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        return {"reply": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
