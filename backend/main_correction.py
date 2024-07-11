import json
import logging
from datetime import datetime

import fastapi
import ollama
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

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

client = OpenAI()


@app.get("/")
def generate_quiz(model: str, euroYear: int):
    prompt = create_prompt(euroYear)

    if model == "mistral":
        questions = None
        while not questions:
            logger.info("Sending to local Ollama server, waiting for response...")

            response = ollama.generate(model="mistral", prompt=f"cree a quiz sur l'euro {euroYear}", format="json")

        return response

    if model == "gpt-4o":
        logger.info("Sending to GPT-4o API, waiting for response...")

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"cree a quiz sur l'euro {euroYear}"}],
            #response_format={"type": "json_object"},
        )

        questions_str = completion.choices[0].message.content

        logger.info(f"GPT-4o answer received")
        return questions_str

    if model == "mock":
        try:
            with open("mockQuestions.json", "r") as file:
                questions = json.load(file)

            logger.info("Quiz generated from mockQuestions.json")
            return questions["quiz"]

        except FileNotFoundError:
            logger.error("mockQuestions.json file not found.")
            return None

    logger.error("Unknown model.")
    return None
