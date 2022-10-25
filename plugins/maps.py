import googlemaps
import database
import datetime
import string
import json


class GoogleMaps:
    dir_cache = "./plugins/cache/maps/"

    def __init__(self, cod_entrega: int = None, **entrega):
        """Gera os datasets contendo as rotas de entrega e as suas informações."""
        self.__id_entrega = cod_entrega
        if cod_entrega is not None:
            self.__cache_carregar()
        else:
            self.erro = False
            maps = googlemaps.Client("AIzaSyD9j77oIrgO1-fAXb4V3af9srmuJArBp_4")
            try:
                self.__response = maps.directions(
                    origin=entrega["origem"],
                    destination=entrega["destino"],
                    mode="driving",
                    waypoints=entrega["paradas"],
                    alternatives=True,
                    language="pt-br",
                    units="metric",
                    departure_time=datetime.datetime.now(),
                    optimize_waypoints=True,
                    traffic_model="best_guess"
                    )
                self.rota_organizada = self.__filtro_organizado()
                self.rota_dataframe = self.__filtro_dataframe()
                if len(self.rota_dataframe) == 0:
                    self.erro = "A rota indicada não pôde ser encontrada por um problema na API do Google Maps."
                else:
                    self.__id_entrega = self.__ultimo_id()
                    self.__cache_criar()
            except Exception as err:
                self.erro = str(err)

    def __ultimo_id(self):
        banco_dados = database.BancoDados()
        id = banco_dados.entregas_id()
        banco_dados.finalizar()
        return id

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
        """Converte os dados da rota para um data frame utilizável pelo Plotly."""
        def _extrair(lista: list, *itens):
            for i in itens:
                lista.extend(i)
            return lista

        dataframe = list()
        for rota in self.rota_organizada:
            coordenadas = [parada["coordenadas"] for parada in rota["paradas"]]
            coordenadas_extraidas = _extrair([], *coordenadas)
            dataframe.append({
                "linhas": {
                    "nome": f"Rota {rota['index']}",
                    "lat": [coord["lat"] for coord in coordenadas_extraidas],
                    "lon": [coord["lon"] for coord in coordenadas_extraidas]
                    },
                "pontos": {
                    "partida": {
                        "lat": coordenadas[0][0]["lat"],
                        "lon": coordenadas[0][0]["lon"]
                        },
                    "lat": [coord[-1]["lat"] for coord in coordenadas],
                    "lon": [coord[-1]["lon"] for coord in coordenadas]
                    }
                })
        return dataframe
    
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
