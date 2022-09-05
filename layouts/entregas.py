from dash import html, dcc
from dash.html import Br


def entregas_layout() -> html.Div:
    """
    Painel de entregas da transportadora contendo informações e análises sobre
    cada uma das viagens registradas no banco de dados - tempo de viagem, rotas
    alternativas, custos totais, mapa interativo com pontos de entrega, etc.
    """
    return html.Div(className="page-entregas", children=[
        html.H3("Página de Entregas")
        ])
