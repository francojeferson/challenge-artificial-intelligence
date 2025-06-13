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

# Configure logging for the web app to align with other modules
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/api/message")
async def post_message(user_input: UserInput):
    user_message = user_input.message
    logger.info(f"Received user message: {user_message}")

    # Define default values for prompt to avoid UnboundLocalError in case of exception
    prompt = "Oi! Como posso te ajudar com programação hoje?"
    content = None

    try:
        from adaptive_learning.prompt.prompt_engine import PromptEngine
        from adaptive_learning.indexing.index_manager import IndexManager

        # Initialize or retrieve the PromptEngine instance for this user
        # For simplicity, create a new instance per request; in production, maintain user sessions
        # TODO: Implement session management to persist user context across requests using user_id
        engine = PromptEngine()
        index_manager = IndexManager()
        from adaptive_learning.content_generation.content_generator import (
            ContentGenerationFactory,
        )

        content_generator = ContentGenerationFactory.get_generator("text")
        engine.content_generator = content_generator
        engine.set_indexed_data(index_manager)

        # Process user interaction through the PromptEngine
        response_data = engine.process_user_interaction(user_message)

        # Extract prompt and content from the response
        prompt = response_data.get(
            "prompt", "Oi! Como posso te ajudar com programação hoje?"
        )
        content = response_data.get("content", None)

        if content and isinstance(content, dict):
            response_text = f"{content.get('title', 'Conteúdo')}: {content.get('content', 'Conteúdo não disponível no momento.')}"
            if content.get("type"):
                response_text = (
                    f"Tipo: {content.get('type').capitalize()}\n{response_text}"
                )
        else:
            response_text = (
                content
                if isinstance(content, str)
                else "Desculpe, não consegui encontrar conteúdo relevante no momento. Pode me dar mais detalhes sobre o que você precisa?"
            )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        response_text = "Ops, algo deu errado ao processar sua mensagem. Que tal tentar de novo ou explicar de outra forma? Estou aqui pra ajudar!"

    return {"response": response_text, "prompt": prompt}
