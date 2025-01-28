import requests
import re
from bs4 import BeautifulSoup

from dotenv import load_dotenv
import os


def retrieve_euro_data(year):
    url = ""
    if year == 1960 or year == 1964:
        url = (
            "https://fr.wikipedia.org/wiki/Coupe_d%27Europe_des_nations_de_football_"+ str(year)
        )
    else:
        url = "https://fr.wikipedia.org/wiki/Championnat_d%27Europe_de_football_" + str(year)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join([p.get_text() for p in soup.find_all("p")])
    return text


def rag_pipeline(year: int, rag_cache: dict, enableRAG: bool):
    prompt = (
        open(os.path.join("..", "prompt-3.txt"), "r")
        .read()
        .replace("{{euroYear}}", str(year))
    )
    if enableRAG:
        if year not in rag_cache:
            rag_cache[year] = retrieve_euro_data(year)
        prompt = rag_cache[year] + prompt
    return prompt


def load_env(file_path=os.path.join("..", ".env")):
    load_dotenv(file_path)
    return {
        key: value for key, value in os.environ.items() if key in open(file_path).read()
    }
