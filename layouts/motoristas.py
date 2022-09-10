from dash import html, dcc
from dash.html import Br


def motoristas_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(className="painel-motoristas", children=[
        html.H1(children="Motoristas")
        ])
