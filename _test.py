import googlemaps
import database
import datetime
import string


class GoogleMaps:
    dir_cache = "./plugins/cache/maps/"

    def __init__(self, cod_entrega: int):
        """Gera os datasets contendo as rotas de entrega e as suas informações."""
        self.id_entrega = cod_entrega
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
            for parada in rota["legs"]:
                coordenadas = list()
                for ponto in parada["steps"]:
                    coordenadas.append({
                        "latitude": ponto["end_location"]["lat"],
                        "longitude": ponto["end_location"]["lng"]
                        })
                else:
                    coordenadas.insert(0, {
                        "latitude": parada["start_location"]["lat"],
                        "longitude": parada["start_location"]["lng"]
                        })

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


if __name__ == '__main__':
    rota = GoogleMaps(1)
