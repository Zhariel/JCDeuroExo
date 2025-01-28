from ollama import chat
from ollama import ChatResponse
import openai
import os
import json
import logging

from utils import retrieve_euro_data, rag_pipeline


def query_mistral(year: int, rag_cache: dict, enableRAG: bool):
    prompt = rag_pipeline(year, rag_cache, enableRAG)
    logger = logging.getLogger(__name__)

    response: ChatResponse = chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    response = response["message"]["content"].replace("`", "")

    try:
        with open(
            os.path.join("quizzes", f"euro-{year}.json"), "w", encoding="utf-8"
        ) as f:
            f.write(response)
        quiz = json.loads(response)
        return quiz["quiz"]
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except KeyError as e:
        logger.error(f"Unexpected response format: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


def query_openai(year: int, api_key: str, rag_cache: dict, enableRAG: bool):
    prompt = rag_pipeline(year, rag_cache, enableRAG)
    logger = logging.getLogger(__name__)

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message["content"].replace("`", "")
        return json.loads(content)["quiz"]
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None
