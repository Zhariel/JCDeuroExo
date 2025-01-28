import os
import json
import logging
import openai

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from llm_handler import query_mistral, query_openai
from utils import load_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = fastapi.FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_data_cache = {}
env = load_env()


@app.get("/")
def generate_quiz(model: str, euroYear: int, enableRAG: bool):
    if model == "mistral":
        response = query_mistral(euroYear, rag_data_cache, enableRAG)
        return response

    if model == "gpt-4o":
        openai_secret = env["OPENAI_SECRET"]
        response = query_openai(euroYear, openai_secret, rag_data_cache, enableRAG)
        return response

    if model == "mock":
        try:
            with open("mockQuestions.json", "r") as file:
                questions = json.load(file)
            logger.info("Quiz generated from mockQuestions.json")
            return questions["quiz"]

        except FileNotFoundError:
            logger.error("mockQuestions.json file not found.")
            return None

    logger.error("Unknown model: %s", model)
    return None
