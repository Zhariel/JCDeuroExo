import requests
import re
from bs4 import BeautifulSoup

def retrieve_euro_data(year):
    url = ""
    if year == 1960 or year == 1964:
        url = "https://fr.wikipedia.org/wiki/Coupe_d%27Europe_des_nations_de_football_" + str(year)
    else: 
        url = "https://fr.wikipedia.org/wiki/Championnat_d%27Europe_de_football_" + str(year)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join([p.get_text() for p in soup.find_all("p")])
    return text