import plotly.express as px
import pandas as pd
from dash import html, dcc
from dash.html import Br


def entregas_layout() -> html.Div:
    """
    Painel de entregas da transportadora contendo informações e análises sobre
    cada uma das viagens registradas no banco de dados - tempo de viagem, rotas
    alternativas, custos totais, mapa interativo com pontos de entrega, etc.
    """
    return html.Div(className="painel-entregas",children=[
        html.Div(className="box-escolha", children=[
            html.H1(children="Entregas"),
            html.P(children="Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do banco de dados."),
            dcc.Dropdown(id="dropdown-entregas")
            ]),
        html.Div(className="box-mapa", children=[
            html.H2(children="Rotas de Entrega"),
            dcc.Graph(className="mapa", id="mapa-entregas")
            ])
        ])
