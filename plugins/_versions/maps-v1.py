import googlemaps
import database
import datetime
import string
import json
import os


class GoogleMaps:
    dir_cache = "./plugins/cache/maps/"

    def __init__(self, cod_entrega: int):
        """Gera os datasets contendo as rotas de entrega e as suas informações."""
        self.__id_entrega = cod_entrega
        if self.__cache_existe():
            self.__cache_carregar()
        else:
            banco_dados = self.__banco_dados()
            maps = googlemaps.Client("AIzaSyD9j77oIrgO1-fAXb4V3af9srmuJArBp_4")
            self.__response = maps.directions(
                origin=banco_dados[0],
                destination=banco_dados[1],
                mode="driving",
                waypoints=banco_dados[2],
                alternatives=True,
                language="pt-br",
                units="metric",
                departure_time=datetime.datetime.now(),
                optimize_waypoints=True,
                traffic_model="best_guess"
                )
            self.rota_organizada = self.__filtro_organizado()
            self.rota_dataframe = self.__filtro_dataframe()
            self.__cache_criar()

    def __banco_dados(self) -> list:
        """Conecta-se com o banco de dados retornando as informações necessárias."""
        banco_dados = database.BancoDados()
        entrega = banco_dados.entregas_busca(self.__id_entrega)
        dados_maps = [entrega[3], entrega[4]]
        if entrega[8].strip() == "Sem parada":
            dados_maps.append([])
        else:
            paradas = entrega[8].split("/")
            dados_maps.append(paradas)
        banco_dados.finalizar()
        return dados_maps

    def __filtro_organizado(self) -> list[dict]:
        """Converte os dados da rota para uma lista de dicionários ordenada."""
        rotas_organizadas = list()
        for letra, rota in zip(string.ascii_uppercase, self.__response):
            rota_paradas = list()
            for index, parada in enumerate(rota["legs"]):
                coordenadas_parada = [{
                    "lat": parada["steps"][0]["start_location"]["lat"],
                    "lon": parada["steps"][0]["start_location"]["lng"]
                    }]
                for coordenada in parada["steps"]:
                    coordenadas_parada.append({
                        "lat": coordenada["end_location"]["lat"],
                        "lon": coordenada["end_location"]["lng"]
                        })
                else:
                    rota_paradas.append({
                        "index": index + 1,
                        "parada": parada["end_address"],
                        "distância": parada["distance"]["value"],
                        "duração": parada["duration"]["value"],
                        "coordenadas": coordenadas_parada
                        })
            rotas_organizadas.append({
                "index": letra,
                "distância": sum([parada["distância"] for parada in rota_paradas]),
                "duração": sum([parada["duração"] for parada in rota_paradas]),
                "paradas": rota_paradas
                })
        return rotas_organizadas

    def __filtro_dataframe(self) -> list[dict]:
        """Converte os dados da rota para um data frame válido pelo Plotly."""
        dataframe = list()
        for rota in self.rota_organizada:
            for pontos in [parada["coordenadas"] for parada in rota["paradas"]]:
                for ponto in pontos:
                    dataframe.append({
                        "Rota": rota["index"],
                        "Distância": rota["distância"],
                        "Tempo": rota["duração"],
                        "Latitude": ponto["lat"],
                        "Longitude": ponto["lon"]
                        })
        return dataframe

    def __cache_existe(self) -> bool:
        """Verifica se há ou não um cache já criado para a entrega analisada."""
        arquivos = os.listdir(GoogleMaps.dir_cache)
        nome_cache = f"maps_ID#{self.__id_entrega}.json"
        if nome_cache in arquivos:
            return True
        else:
            return False
    
    def __cache_carregar(self) -> None:
        """Carrega o cache da entrega analisada caso este já tenha sido criado."""
        with open(f"{GoogleMaps.dir_cache}maps_ID#{self.__id_entrega}.json", "r") as cache:
            json_data = json.load(cache)
            self.rota_organizada = json_data["organizada"]
            self.rota_dataframe = json_data["dataframe"]
    
    def __cache_criar(self) -> None:
        """Cria o cache da entrega analisada para uso posterior, poupando requests da API."""
        with open(f"{GoogleMaps.dir_cache}maps_ID#{self.__id_entrega}.json", "w") as cache:
            json_data = {
                "organizada": self.rota_organizada,
                "dataframe": self.rota_dataframe
                }
            json.dump(json_data, cache)
