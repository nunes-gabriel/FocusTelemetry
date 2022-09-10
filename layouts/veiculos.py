from dash import html, dcc
from dash.html import Br


def veiculos_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(className="painel-veiculos", children=[
        html.H1(children="Veículos")
        ])
