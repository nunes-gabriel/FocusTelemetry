import json

"""
Chaves do Response:
| bounds ('limites')
| copyrights ('direitos')
|-> legs ('pernas')
| overview_polyline ('visão geral')
| summary ('sumário')
| warnings ('avisos')
|-> waypoint_order ('ordem das paradas')

Chaves do Response["legs"]:
| distance
| duration
| end_address
| end_location
| start_address
| start_location
| steps
| traffic_speed_entry
| via_waypoint
"""


def main(response_bruto: list[dict]):
    numero_rotas = response_bruto.__len__()
    for rota in response_bruto:
        print(rota["waypoint_order"])
        viagens = rota["legs"]
        for numero, viagem in enumerate(viagens):
            print(f"Viagem {numero + 1}:")
            print(f"Local Final - {viagem['end_location']}")
            print(f"Local Inicial - {viagem['start_location']}", end="\n\n\n")


def filtro_organizado(response_bruto: list[dict]):
    rotas_organizadas = list()
    for rota in response_bruto:
        for numero, viagem in enumerate(rota["legs"]):
            pass


if __name__ == "__main__":
    with open("./plugins/cache/maps/teste2.json", "r") as arquivo:
        response = json.load(arquivo)
        main(response)
