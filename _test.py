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
            lista_paradas = []
            for numero, parada in enumerate(rota["legs"]):
                coordenadas = list()
                for ponto in parada["steps"]:
                    coordenadas.append({
                        "latitude": ponto["end_location"]["lat"],
                        "longitude": ponto["end_location"]["lng"]
                        })
                else:
                    coordenadas.insert(0, {
                        "latitude": ponto["start_location"]["lat"],
                        "longitude": ponto["start_location"]["lng"]
                        })
                lista_paradas.append({
                    "nome": f"Parada {numero}",
                    "distancia": parada["distance"]["value"],
                    "tempo": parada["duration"]["value"],
                    "coordenadas": coordenadas
                    })
            rotas_ordenadas.append({
                "nome": f"Rota {letra}",
                "distancia": sum([parada["distancia"] for parada in lista_paradas]),
                "tempo": sum([parada["tempo"] for parada in lista_paradas]),
                "paradas": lista_paradas
                })
        return rotas_ordenadas

    def __filtro_dataframe(self) -> list[dict]:
        """Converte os dados da rota para um data frame válido pelo Plotly."""
        dataframe = list()
        for rota in self.filtro_ordenadas:
            for pontos in [parada["coordenadas"] for parada in rota["paradas"]]:
                for ponto in pontos:
                    dataframe.append({
                        "nome": rota["nome"],
                        "distancia": rota["distancia"],
                        "tempo": rota["tempo"],
                        "latitude": ponto["latitude"],
                        "longitude": ponto["longitude"]
                        })
        return dataframe


if __name__ == '__main__':
    rota = GoogleMaps(1)
    print(rota.filtro_ordenadas)
    print(rota.filtro_dataframe)
