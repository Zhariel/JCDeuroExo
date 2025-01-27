import os
import json
import logging

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from mistral_handler import query_mistral

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

@app.get("/")
def generate_quiz(model: str, euroYear: int, enableRAG: bool):
    print(enableRAG)
    use_rag = True
    if model == "mistral":
        try:
            logger.info("Generating quiz with mistral")
            quiz = query_mistral(euroYear, rag_data_cache, use_rag)
            logger.info("Done generating quiz")
            return quiz["quiz"]
        except Exception as e:
            logger.error(e)
            return None

    if model == "gpt-4o":
        pass

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
