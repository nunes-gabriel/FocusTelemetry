from dash import html, dcc
from dash.html import Br


def banco_dados_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(className="painel-banco-dados", children=[
        html.H1(children="Banco de Dados")
        ])
