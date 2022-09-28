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


def main():
    with open("./plugins/cache/maps/teste.json", "r") as arquivo:
        response = json.load(arquivo)
        numero_rotas = response.__len__()
        for rota in response:
            viagens = rota["legs"]
            for numero, viagem in enumerate(viagens):
                print(f"{numero}:")
                print(f"Local Final - {viagem['end_location']}")
                print(f"Local Inicial - {viagem['start_location']}")
                print("\n\n")


if __name__ == "__main__":
    main()
