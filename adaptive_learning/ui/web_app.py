from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

# Mount static files directory for React build
app.mount(
    "/static",
    StaticFiles(directory="adaptive_learning/ui/frontend/build/static"),
    name="static",
)

templates = Jinja2Templates(directory="adaptive_learning/ui/frontend/build")


class UserInput(BaseModel):
    message: str
    user_id: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


import json
import re


import logging


@app.post("/api/message")
async def post_message(user_input: UserInput):
    user_message = user_input.message.lower()
    logging.info(f"Received user message: {user_message}")

    try:
        if "html" in user_message:
            with open("resources/Apresentação.txt", "r", encoding="utf-8") as f:
                content = f.read()
            response_text = content[:700] + "..."
        elif (
            "exercício" in user_message
            or "exercicios" in user_message
            or "questão" in user_message
        ):
            with open("resources/Exercícios.json", "r", encoding="utf-8") as f:
                exercises = json.load(f)
            first_question = exercises["content"][0]
            question_title = first_question.get("title", "Questão")
            question_html = first_question["content"].get("html", "")
            question_text = re.sub(r"<[^>]+>", "", question_html).strip()
            response_text = f"{question_title}: {question_text}"
        elif "vídeo" in user_message or "video" in user_message:
            response_text = "Você prefere aprender com vídeos? Temos dicas de professores em vídeo para você."
        else:
            response_text = (
                "Conteúdo adaptativo será gerado aqui com base nas suas necessidades."
            )
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        response_text = "Desculpe, ocorreu um erro ao processar sua solicitação."

    return {"response": response_text}
