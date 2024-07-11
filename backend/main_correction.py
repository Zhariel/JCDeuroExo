import json
import logging
from datetime import datetime

import fastapi
import jsonschema
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


def create_prompt(euroYear):
    return """
    # Rôle
    Tu es un excellent créateur de quiz sur le football et sur l'Euro %s.

    # Objectif
    Crée un quiz sur l'Euro %s de 5 questions à choix multiples. Les questions ont 4 options avec une seule réponse juste. Il faut indiquer pour chaque option si elle est juste. Pour chaque question, il faut donner du contexte ou des informations supplémentaires permettant d'éclairer la bonne réponse. Ce quiz doit être grand public.

    # Format
    Donne ta réponse sous la forme d'un objet JSON avec l'unique clé "quiz". La valeur associée à "quiz" doit être un tableau (array) d'objets. Chaque élément de ce tableau doit être un objet avec les clés suivantes :
    - "question" : une chaîne de caractères représentant la question posée
    - "options" : un tableau d'objets représentant les options de réponse possibles. Chaque objet doit contenir les clés suivantes :
        - "text" : une chaîne de caractères représentant le texte de l'option de réponse
        - "isCorrect" : un booléen indiquant si l'option de réponse est correcte (true) ou incorrecte (false)
    - "context" : une chaîne de caractères fournissant un contexte ou une explication supplémentaire concernant la question

    # Exemple d'une seule question
    {
    "question": "Dans quels pays s'est tenu l'UEFA Euro 2000 ?",
    "options": [
        {
        "text": "Angleterre et Écosse",
        "isCorrect": false
        },
        {
        "text": "France et Allemagne",
        "isCorrect": false
        },
        {
        "text": "Belgique et Pays-Bas",
        "isCorrect": true
        },
        {
        "text": "Espagne et Portugal",
        "isCorrect": false
        }
    ],
    "context": "L'UEFA Euro 2000 a été le premier championnat d'Europe à être organisé par plusieurs nations, avec la Belgique et les Pays-Bas comme co-organisateurs."
    }
    """ % (euroYear, euroYear)


schema = {
    "type": "object",
    "properties": {
        "quiz": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "isCorrect": {"type": "boolean"},
                            },
                            "required": ["text", "isCorrect"],
                        },
                    },
                    "context": {"type": "string"},
                },
                "required": ["question", "options", "context"],
            },
        }
    },
    "required": ["quiz"],
}


def verify_json(json_string):
    try:
        # Load the JSON data and validate it against the schema
        json_data = json.loads(json_string)
        jsonschema.validate(json_data, schema)
        return json_data

    except json.JSONDecodeError:
        logger.error("Error: The json string is not a valid JSON.")
        return None
    except jsonschema.ValidationError:
        logger.error("Error: The JSON data does not match the schema.")
        return None


@app.get("/")
def generate_quiz(model: str, euroYear: int):
    prompt = create_prompt(euroYear)

    if model == "mistral":
        questions = None
        while not questions:
            logger.info("Sending to local Ollama server, waiting for response...")

            start_time = datetime.now()
            response = ollama.generate(model="mistral", prompt=prompt, format="json")
            end_time = datetime.now()

            questions_str = response["response"]
            questions = verify_json(questions_str)

            logger.info(f"Ollama answer received in {end_time - start_time}")
        return questions["quiz"]

    if model == "gpt-4o":
        logger.info("Sending to GPT-4o API, waiting for response...")

        start_time = datetime.now()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        end_time = datetime.now()

        questions_str = completion.choices[0].message.content
        questions = verify_json(questions_str)

        logger.info(f"GPT-4o answer received in {end_time - start_time}")
        return questions["quiz"]

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
