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
        self.id_entrega = cod_entrega
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
            self.filtro_ordenadas = self.__filtro_ordenadas()
            self.filtro_dataframe = self.__filtro_dataframe()
            self.__cache_criar()

    def __banco_dados(self) -> list:
        """Conecta-se com o banco de dados retornando as informações necessárias."""
        banco_dados = database.BancoDados()
        entrega = banco_dados.entregas_busca(self.id_entrega)
        dados_maps = [entrega[3], entrega[4]]
        if entrega[-2].strip() == "Sem parada":
            dados_maps.append([])
        else:
            dados_maps.append(entrega[-2])
        banco_dados.finalizar()
        return dados_maps

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

    def __cache_existe(self) -> bool:
        """Verifica se há ou não um cache já criado para a entrega analisada."""
        arquivos = os.listdir(GoogleMaps.dir_cache)
        nome_cache = f"maps_ID#{self.id_entrega}.json"
        if nome_cache in arquivos:
            return True
        else:
            return False
    
    def __cache_carregar(self) -> None:
        """Carrega o cache da entrega analisada caso este já tenha sido criado."""
        with open(f"{GoogleMaps.dir_cache}maps_ID#{self.id_entrega}.json", "r") as cache:
            json_data = json.load(cache)
            self.filtro_ordenadas = json_data["ordenadas"]
            self.filtro_dataframe = json_data["dataframe"]
    
    def __cache_criar(self) -> None:
        """Cria o cache da entrega analisada para uso posterior, poupando requests da API."""
        with open(f"{GoogleMaps.dir_cache}maps_ID#{self.id_entrega}.json", "w") as cache:
            json_data = {
                "ordenadas": self.filtro_ordenadas,
                "dataframe": self.filtro_dataframe
                }
            json.dump(json_data, cache)
