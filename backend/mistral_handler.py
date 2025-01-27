from ollama import chat
from ollama import ChatResponse
import os
import json
import logging

from utils import retrieve_euro_data


def query_mistral(year: str, rag_cache: dict, use_rag: bool):
    prompt = (
        open(os.path.join("..", "prompt-3.txt"), "r")
        .read()
        .replace("{{euroYear}}", str(year))
    )

    logger = logging.getLogger(__name__)
    
    logger.info("generating")
    
    if use_rag:
        if year not in rag_cache:
            rag_cache[year] = retrieve_euro_data(year)
        prompt = rag_cache[year] + prompt

    response: ChatResponse = chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    
    response = response["message"]["content"].replace("`", '')
    
    try:
        with open(os.path.join("quizzes", f"euro-{year}.json"), "w", encoding="utf-8") as f:
            f.write(response)
        quiz = json.loads(response)
        return quiz
    except json.JSONDecodeError as e:
        logger = logging.getLogger(__name__)
        logger.error("Error decoding json.")
        logger.error(f"Message: {e.msg}")
        return None