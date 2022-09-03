from dash import html, dcc
from dash.html import Br


def entregas():
    """Um painel com informações sobre viagens em andamento da transportadora"""
    return html.Div(className="page-entregas", children=[
        dcc.Link(className="retornar-index", href="/", children="Voltar"), Br(),
        html.H3("Página de Entregas")
        ])
