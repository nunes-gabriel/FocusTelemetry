from googlemaps import Client
from datetime import datetime
from string import ascii_uppercase
from json import dump, load
from os import listdir


def rotas_viagem(cod_entrega: int, ponto_partida: str, ponto_chegada: str, paradas: list[str] = []) -> list:
    if log_verificar(cod_entrega):
        return log_ler(cod_entrega)
    else:
        gmaps = Client("AIzaSyD9j77oIrgO1-fAXb4V3af9srmuJArBp_4")
        response = gmaps.directions(
            origin=ponto_partida,
            destination=ponto_chegada,
            mode="driving",
            waypoints=paradas,
            alternatives=True,
            language="pt-br",
            units="metric",
            departure_time=datetime.now(),
            optimize_waypoints=True,
            traffic_model="best_guess"
            )
        log_criar(cod_entrega, response)
        return response


def filtrar_response(response: dict):
    response_filtrado = list()
    for index_nome, rota in enumerate(response):
        data_bruto = rota["legs"][0]
        pontos = data_bruto["steps"]
        for index_ponto, ponto in enumerate(pontos):
            if index_ponto == 0:
                response_filtrado.append({
                    "nome": f"Rota {ascii_uppercase[index_nome]}",
                    "distancia": data_bruto["distance"]["value"],
                    "tempo": data_bruto["duration"]["value"],
                    "latitude": ponto["start_location"]["lat"],
                    "longitude": ponto["start_location"]["lng"]
                    })
            response_filtrado.append({
                "nome": f"Rota {ascii_uppercase[index_nome]}",
                "distancia": data_bruto["distance"]["value"],
                "tempo": data_bruto["duration"]["value"],
                "latitude": ponto[["start_location" if index_ponto == 0 else "end_location"]]["lat"],
                "longitude": ponto["end_location"]["lng"]
                })
    else:
        return response_filtrado


def log_verificar(cod_entrega: int) -> bool:
    logs_dir = listdir("./plugins/logs/maps/")
    if f"maps_log#{cod_entrega}.json" in logs_dir:
        return True
    else:
        return False


def log_ler(cod_entrega: int):
    with open(f"./plugins/logs/maps/maps_log#{cod_entrega}.json", "r") as log:
        return load(log)


def log_criar(cod_entrega: int, response: list):
    with open(f"./plugins/logs/maps/maps_log#{cod_entrega}.json", "w") as log:
        dump(response, log)
