from bs4 import BeautifulSoup
import requests


class Scraping:
    websites = [
        "https://precos.petrobras.com.br/sele%C3%A7%C3%A3o-de-estados-gasolina",
        "https://precos.petrobras.com.br/sele%C3%A7%C3%A3o-de-estados-diesel"
        ]

    def __init__(self):
        self.__dados_scraping = dict()
        for website, tipo in zip(Scraping.websites, ["Gasolina", "Diesel"]):
            response = requests.get(website)
            html = BeautifulSoup(response.text, "html.parser")
            preco = html.select("#telafinal-precofinal")[0]
            preco = float(preco.text.strip().replace(",", "."))
            self.__dados_scraping[tipo] = preco

    def __getitem__(self, tipo: str):
        return self.__dados_scraping[tipo]
