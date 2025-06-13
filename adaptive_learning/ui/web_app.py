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
    format: Optional[str] = "text"


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


import json
import re


import logging

# Configure logging for the web app to align with other modules
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/api/feedback")
async def post_feedback(feedback_input: UserInput):
    feedback_message = feedback_input.message
    user_id = feedback_input.user_id
    format_preference = feedback_input.format
    logger.info(
        f"Received feedback: {feedback_message} from user {user_id if user_id else 'anonymous'} with format preference: {format_preference}"
    )

    # For now, just log the feedback; in production, store in a database
    feedback_file = "feedback_log.json"
    feedback_entry = {
        "user_id": user_id if user_id else "anonymous",
        "feedback": feedback_message,
        "format_preference": format_preference,
        "timestamp": str(os.times().system),
    }

    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, "r") as f:
                feedback_data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading feedback file: {str(e)}")
            feedback_data = []
    else:
        feedback_data = []

    feedback_data.append(feedback_entry)
    try:
        with open(feedback_file, "w") as f:
            json.dump(feedback_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error writing to feedback file: {str(e)}")

    return {
        "status": "success",
        "message": "Obrigado pelo seu feedback! Sua opinião é muito importante para nós.",
    }


@app.post("/api/message")
async def post_message(user_input: UserInput):
    user_message = user_input.message
    user_format = user_input.format
    user_id = user_input.user_id
    logger.info(
        f"Received user message: {user_message}, preferred format: {user_format}"
    )

    # Define default values for prompt to avoid UnboundLocalError in case of exception
    prompt = "Oi! Como posso te ajudar com programação hoje?"
    content = None

    # Simple in-memory cache for responses
    from collections import OrderedDict

    if not hasattr(post_message, "cache"):
        post_message.cache = OrderedDict()
        post_message.cache_size = 100  # Limit cache size to prevent memory issues

    # Create a cache key based on user message and format
    cache_key = (user_message, user_format)
    if cache_key in post_message.cache:
        logger.info(f"Cache hit for message: {user_message}")
        cached_response = post_message.cache[cache_key]
        return {
            "response": cached_response["response"],
            "prompt": cached_response["prompt"],
        }

    logger.info(f"Cache miss for message: {user_message}, processing request.")

    try:
        from adaptive_learning.prompt.prompt_engine import PromptEngine
        from adaptive_learning.indexing.index_manager import IndexManager

        # Session data is managed on the client side using localStorage
        # No need for server-side session storage
        session_data = {}

        engine = PromptEngine()
        index_manager = IndexManager()
        from adaptive_learning.content_generation.content_generator import (
            ContentGenerationFactory,
        )

        content_generator = ContentGenerationFactory.get_generator(user_format)
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

        # Session data is managed on the client side, no server-side saving needed
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        response_text = "Ops, algo deu errado ao processar sua mensagem. Que tal tentar de novo ou explicar de outra forma? Estou aqui pra ajudar!"

    # Store response in cache before returning
    response_data = {"response": response_text, "prompt": prompt}
    post_message.cache[cache_key] = response_data
    if len(post_message.cache) > post_message.cache_size:
        post_message.cache.popitem(last=False)  # Remove least recently used item

    return response_data
