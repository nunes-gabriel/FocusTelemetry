from bs4 import BeautifulSoup
import requests
import datetime
import json
import os


class Scraping:
    dir_logs = "./plugins/logs/scraping/"
    websites = [
        "https://precos.petrobras.com.br/sele%C3%A7%C3%A3o-de-estados-gasolina",
        "https://precos.petrobras.com.br/sele%C3%A7%C3%A3o-de-estados-diesel"
        ]

    def __init__(self):
        self.dados_scraping = dict()
        for website, tipo in zip(Scraping.websites, ["Gasolina", "Diesel"]):
            response = requests.get(website)
            html = BeautifulSoup(response.text, "html.parser")
            preco = html.select("#telafinal-precofinal")[0]
            preco = float(preco.text.strip().replace(",", "."))
            self.dados_scraping[tipo] = preco

        @classmethod
        def __log_verificar(cls):
            """Verifica se há ou não um log já criado nas últimas 24 horas para os preços."""
            arquivos = os.listdir(Scraping.dir_logs)
            data_atual = datetime.datetime.now()
            nome_log = f"log_scraping#{data_atual.date()}/{data_atual.time()}.json"
            if nome_log in arquivos:
                return True
            else:
                return False

        @classmethod
        def __log_carregar(cls):
            """Carrega o último log de preços caso este tenha sido criado nas últimas 24 horas."""
            data_atual = datetime.datetime.now()
            with open(f"{Scraping.dir_logs}log_scraping#{data_atual.date()}/{data_atual.time()}.json", "r") as log:
                json_data = json.load(log)
                self.dados_scraping = json_data["scraping"]

        @classmethod
        def __log_criar(cls):
            """Cria o log de preços com duração de 24 horas, poupando requests e gerando um banco de dados."""
            data_atual = datetime.datetime.now()
            with open(f"{Scraping.dir_logs}log_scraping#{data_atual.date()}/{data_atual.time()}.json", "w") as log:
                json_data = {
                    "data": data_atual,
                    "scraping": self.dados_scraping
                    }
                json.dump(json_data, log)
