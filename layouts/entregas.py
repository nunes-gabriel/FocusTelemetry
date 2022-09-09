import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc
from dash.html import Br


def entregas_layout() -> html.Div:
    """
    Painel de entregas da transportadora contendo informações e análises sobre
    cada uma das viagens registradas no banco de dados - tempo de viagem, rotas
    alternativas, custos totais, mapa interativo com pontos de entrega, etc.
    """

    # global lista_estados
    # lista_estados = {
    #     "AC": {"lat": -8.77, "lon": -70.55},
    #     "AL": {"lat": -9.71, "lon": -35.73},
    #     "AM": {"lat": -3.07, "lon": -61.66},
    #     "AP": {"lat": 1.41, "lon": -51.77},
    #     "BA": {"lat": -12.96, "lon": -38.51},
    #     "CE": {"lat": -3.71, "lon": -38.54},
    #     "DF": {"lat": -15.83, "lon": -47.86},
    #     "ES": {"lat": -19.19, "lon": -40.34},
    #     "GO": {"lat": -16.64, "lon": -49.31},
    #     "MA": {"lat": -2.55, "lon": -44.30},
    #     "MT": {"lat": -12.64, "lon": -55.42},
    #     "MS": {"lat": -20.51, "lon": -54.54},
    #     "MG": {"lat": -18.10, "lon": -44.38},
    #     "PA": {"lat": -5.53, "lon": -52.29},
    #     "PB": {"lat": -7.06, "lon": -35.55},
    #     "PR": {"lat": -24.89, "lon": -51.55},
    #     "PE": {"lat": -8.28, "lon": -35.07},
    #     "PI": {"lat": -8.28, "lon": -43.68},
    #     "RJ": {"lat": -22.84, "lon": -43.15},
    #     "RN": {"lat": -5.22, "lon": -36.52},
    #     "RO": {"lat": -11.22, "lon": -62.80},
    #     "RS": {"lat": -30.01, "lon": -51.22},
    #     "RR": {"lat": 1.89, "lon": -61.22},
    #     "SC": {"lat": -27.33, "lon": -49.44},
    #     "SE": {"lat": -10.90, "lon": -37.07},
    #     "SP": {"lat": -23.55, "lon": -46.64},
    #     "TO": {"lat": -10.25, "lon": -48.25}
    #     }

    return html.Div(className="painel-entregas", children=[
        html.H1("Painel de Entregas")
        ])
