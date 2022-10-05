from dash import html, dcc, Input, Output, State
from plotly import express as px

import database
import dash

dash.register_page(
    __name__,
    path="/veiculos",
    path_template="/veiculos/<placa_veiculo>",
    title="Painel de Veículos",
    name="veiculos",
    order=2
    )


def layout(placa_veiculo=None):
    return html.Div(children=[
        html.Div(className="card veiculos--pesquisa", children=[
            html.H1("Veículos"),
            html.P("Escolha um veículo para análise e/ou edição ou cadastre um novo veículo no sistema."),
            html.Div(children=[
                dcc.Dropdown(className="dropdown veiculos--pesquisa", id="veiculos--dropdown", value="Placa", clearable=False),
                dcc.Input(className="input veiculos--pesquisa", id="veiculos--input", type="search", debounce=True,
                    placeholder="Pesquisar por placa...")
                ])
            ]),
        html.Div(className="card veiculos--informacoes", children=[
            html.H1(placa_veiculo)
            ])
        ])
