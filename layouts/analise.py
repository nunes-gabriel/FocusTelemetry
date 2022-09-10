from dash import html, dcc
from dash.html import Br


def analise_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(className="painel-analise", children=[
        html.H1(children="Análise Geral")
        ])
