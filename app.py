from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load .env and API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI app setup
app = FastAPI()

# CORS (so frontend from other domains can call this if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files if needed (e.g., CSS, JS later)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at "/"
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r") as f:
        return f.read()

# Request body model
class Question(BaseModel):
    query: str

# Load your resume content
with open("gary_resume.txt", "r") as f:
    resume_content = f.read()

# Chat endpoint
@app.post("/ask")
async def ask(question: Question):
    prompt = f"Based on the following resume:\n{resume_content}\n\nQ: {question.query}\nA:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['choices'][0]['message']['content']
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
