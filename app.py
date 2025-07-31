
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Question(BaseModel):
    query: str

with open("gary_resume.txt", "r") as f:
    resume_content = f.read()

@app.post("/ask")
async def ask(question: Question):
    prompt = f"Based on the resume:\n{resume_content}\n\nQ: {question.query}\nA:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": response['choices'][0]['message']['content']}
