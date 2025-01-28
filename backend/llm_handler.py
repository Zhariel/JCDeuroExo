from ollama import chat
from ollama import ChatResponse
from openai import OpenAI
from openai import OpenAIError
from jsonschema import validate, ValidationError

import os
import json
import logging

from utils import rag_pipeline


def query_mistral(year: int, rag_cache: dict, enableRAG: bool):
    prompt = rag_pipeline(year, rag_cache, enableRAG, "prompt-3")
    logger = logging.getLogger(__name__)
    with open(os.path.join("quizzes", "schema.json"), 'r') as file:
        schema = json.load(file)

    try:
        response: ChatResponse = chat(
            model="mistral",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        response = response.message.content.replace("`", "")
        
        with open(
            os.path.join("quizzes", f"euro-{year}.json"), "w", encoding="utf-8"
        ) as f:
            f.write(response)
        quiz = json.loads(response)
        validate(instance=quiz, schema=schema)
        return quiz["quiz"]
    except ValidationError as e:
        print(f"Validation error: {e.message}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except KeyError as e:
        logger.error(f"Unexpected response format: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


def query_openai(year: int, api_key: str, rag_cache: dict, enableRAG: bool):
    prompt = rag_pipeline(
        year, rag_cache, enableRAG, "prompt-4"
    )  # prompt tronqué pour respecter la limite de tokens
    logger = logging.getLogger(__name__)
    client = OpenAI(api_key=api_key)
    with open(os.path.join("quizzes", "schema.json"), 'r') as file:
        schema = json.load(file)

    try:
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content.replace("`", "")
        with open(
            os.path.join("quizzes", f"euro-{year}.json"), "w", encoding="utf-8"
        ) as f:
            f.write(content)
            
        quiz = json.loads(content)
        validate(instance=quiz, schema=schema)
        return quiz["quiz"]
    except ValidationError as e:
        print(f"Validation error: {e.message}")
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None
