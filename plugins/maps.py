import googlemaps
import datetime
import string
import json
import os


class GoogleMaps:
    logs_diretorio = "./plugins/logs/maps/"

    def __init__(self, cod_entrega: int, partida: str, chegada: str, paradas: list[str] = []):
        """Gera os datasets contendo as rotas de entrega e suas informações."""
        self.codigo_entrega = str(cod_entrega)
        if self.__existe():
            self.__carregar()
        else:
            maps = googlemaps.Client("AIzaSyD9j77oIrgO1-fAXb4V3af9srmuJArBp_4")
            self.__response = maps.directions(
                origin=partida,
                destination=chegada,
                mode="driving",
                waypoints=paradas,
                alternatives=True,
                language="pt-br",
                units="metric",
                departure_time=datetime.datetime.now(),
                optimize_waypoints=True,
                traffic_model="best_guess"
                )
            self.dicionario = self.__dicionario()
            self.data_frame = self.__data_frame()
            self.__criar()

    def __dicionario(self) -> list[dict]:
        """Converte os dados da rota para uma lista de dicionários legíveis."""
        dicionarios = list()
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
            dicionarios.append({
                "nome": "Rota " + letra,
                "distancia": data_bruto["distance"]["value"],
                "tempo": data_bruto["duration"]["value"],
                "coordenadas": coordenadas
                })
        return dicionarios

    def __data_frame(self) -> list[dict]:
        """Converte os dados da rota para um data frame válido pelo Plotly."""
        data_frame = list()
        for rota in self.dicionario:
            for coordenada in rota["coordenadas"]:
                data_frame.append({
                    "nome": rota["nome"],
                    "distancia": rota["distancia"],
                    "tempo": rota["tempo"],
                    "latitude": coordenada["latitude"],
                    "longitude": coordenada["longitude"]
                    })
        return data_frame

    def __existe(self) -> bool:
        """Verifica se há ou não um log já criado para a entrega analisada."""
        arquivos = os.listdir(GoogleMaps.logs_diretorio)
        nome_log = "log_maps#" + self.codigo_entrega + ".json"
        if nome_log in arquivos:
            return True
        else:
            return False
    
    def __carregar(self) -> None:
        """Carrega o log da entrega analisada caso este já tenha sido criado."""
        with open(GoogleMaps.logs_diretorio + "log_maps#" + self.codigo_entrega + ".json", "r") as log:
            json_data = json.load(log)
            self.dicionario = json_data["dicionario"]
            self.data_frame = json_data["data_frame"]
    
    def __criar(self) -> None:
        """Cria o log da entrega analisada para uso posterior, poupando requests da API."""
        with open(GoogleMaps.logs_diretorio + "log_maps#" + self.codigo_entrega + ".json", "w") as log:
            json_data = {
                "dicionario": self.dicionario,
                "data_frame": self.data_frame
                }
            json.dump(json_data, log)
