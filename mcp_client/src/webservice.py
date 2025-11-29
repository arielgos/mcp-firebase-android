from fastapi import FastAPI
from pydantic import BaseModel
from app.client_openai import chat_with_gemini

app = FastAPI()

class MessageRequest(BaseModel):
    message:str

@app.get("/")
def root():
    return {"message": "Webservice en Python funcionando 🚀"}

@app.post("/chat")
def chat(body: MessageRequest):
    return chat_with_gemini(body.message)
