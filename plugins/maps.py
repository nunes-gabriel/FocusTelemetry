import googlemaps
import datetime
import string
import pandas
import json
import os


class GoogleMaps:
    dir_logs = "./plugins/logs/maps/"

    def __init__(self, cod_entrega: int):
        """Gera os datasets contendo as rotas de entrega e as suas informações."""
        self.id_entrega = cod_entrega
        if self.__log_existe():
            self.__log_carregar()
        else:
            banco_dados = self.__banco_dados()
            maps = googlemaps.Client("AIzaSyD9j77oIrgO1-fAXb4V3af9srmuJArBp_4")
            self.__response = maps.directions(
                origin=banco_dados["ponto_partida"],
                destination=banco_dados["ponto_chegada"],
                mode="driving",
                waypoints=banco_dados["pontos_parada"],
                alternatives=True,
                language="pt-br",
                units="metric",
                departure_time=datetime.datetime.now(),
                optimize_waypoints=True,
                traffic_model="best_guess"
                )
            self.filtro_ordenadas = self.__filtro_ordenadas()
            self.filtro_dataframe = self.__filtro_dataframe()
            self.__log_criar()

    def __banco_dados(self) -> dict:
        """Conecta-se com o banco de dados retornando as informações necessárias."""
        dados = pandas.read_csv("./database/_dataframe.csv", delimiter=";")
        dados_linha = dict(dados.loc[self.id_entrega - 1])
        if dados_linha["pontos_parada"] == "*":
            dados_linha.update({"pontos_parada": []})
        return dados_linha

    def __filtro_ordenadas(self) -> list[dict]:
        """Converte os dados da rota para uma lista de dicionários ordenada."""
        rotas_ordenadas = list()
        for rota, letra in zip(self.__response, string.ascii_uppercase):
            coordenadas = list()
            data_bruto = rota["legs"][0]
            pontos = data_bruto["steps"]
            for ponto in pontos:
                coordenadas.append({
                    "latitude": ponto["end_location"]["lat"],
                    "longitude": ponto["end_location"]["lng"]
                    })
            else:
                coordenadas.insert(0, {
                    "latitude": data_bruto["start_location"]["lat"],
                    "longitude": data_bruto["start_location"]["lng"]
                    })
            rotas_ordenadas.append({
                "nome": "Rota " + letra,
                "distancia": data_bruto["distance"]["value"],
                "tempo": data_bruto["duration"]["value"],
                "coordenadas": coordenadas
                })
        return rotas_ordenadas

    def __filtro_dataframe(self) -> list[dict]:
        """Converte os dados da rota para um data frame válido pelo Plotly."""
        dataframe = list()
        for rota in self.filtro_ordenadas:
            for coordenada in rota["coordenadas"]:
                dataframe.append({
                    "nome": rota["nome"],
                    "distancia": rota["distancia"],
                    "tempo": rota["tempo"],
                    "latitude": coordenada["latitude"],
                    "longitude": coordenada["longitude"]
                    })
        return dataframe

    def __log_existe(self) -> bool:
        """Verifica se há ou não um log já criado para a entrega analisada."""
        arquivos = os.listdir(GoogleMaps.dir_logs)
        nome_log = f"log_maps#{self.id_entrega}.json"
        if nome_log in arquivos:
            return True
        else:
            return False
    
    def __log_carregar(self) -> None:
        """Carrega o log da entrega analisada caso este já tenha sido criado."""
        with open(f"{GoogleMaps.dir_logs}log_maps#{self.id_entrega}.json", "r") as log:
            json_data = json.load(log)
            self.filtro_ordenadas = json_data["ordenadas"]
            self.filtro_dataframe = json_data["dataframe"]
    
    def __log_criar(self) -> None:
        """Cria o log da entrega analisada para uso posterior, poupando requests da API."""
        with open(f"{GoogleMaps.dir_logs}log_maps#{self.id_entrega}.json", "w") as log:
            json_data = {
                "ordenadas": self.filtro_ordenadas,
                "dataframe": self.filtro_dataframe
                }
            json.dump(json_data, log)
