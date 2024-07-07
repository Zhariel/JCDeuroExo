import json
import logging

import fastapi
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def generate_quiz(model: str, euroYear: int):
    if model == "mistral":
        ...

    if model == "gpt-4o":
        ...

    if model == "mock":
        try:
            with open("mockQuestions.json", "r") as file:
                questions = json.load(file)
            logger.info("Quiz generated from mockQuestions.json")
            return questions

        except FileNotFoundError:
            logger.error("mockQuestions.json file not found.")
            return None

    logger.error("Unknown model: %s", model)
    return None
