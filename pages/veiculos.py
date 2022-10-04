from dash import html, dcc, Input, Output, State
from plotly import express as px

import database
import dash

dash.register_page(
    __name__,
    path="/veiculos",
    title="Painel de Veículos",
    name="veiculos",
    order=2
    )


def layout():
    # return html.Div(className="page", children=[

    #     ])

    return html.Div(className="page", children=[
        html.Div(className="modal", style={"display": "none"}, id="veiculos-modal"),
        html.Div(className="col", children=[
            html.Div(className="row", children=[
                dcc.Input(placeholder="Procure por um veículo...", type="search", id="veiculos-pesquisa")
                ]),
            html.Div(className="row", id="veiculos-lista")
            ]),
        html.Div(className="col", id="veiculos-informacoes")
        ])


@dash.callback(
    Output("veiculos-lista", "children"),
    Input("veiculos-pesquisa", "value")
    )
def pesquisar_veiculos(pesquisa: str):
    banco_dados = database.BancoDados()
    return dash.no_update
