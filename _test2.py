import json
import string

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
            print(f"Local Inicial - {viagem['start_location']}")
            print(f"Primeiro passo: {viagem['steps'][0]}", end="\n\n\n")


def filtro_organizado(response_bruto: list[dict]):
    rotas_organizadas = list()
    for letra, rota in zip(string.ascii_uppercase, response_bruto):
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


if __name__ == "__main__":
    with open("./plugins/cache/maps/teste2.json", "r") as arquivo:
        response = json.load(arquivo)
        print(filtro_organizado(response))
