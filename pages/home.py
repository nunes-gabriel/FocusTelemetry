from dash import html, dcc, Input, Output, State

import os
import database
import dash

dash.register_page(
    __name__,
    path="/",
    title="Home",
    name="home",
    order=0
    )


def layout():
    return html.Div(children=[
        dcc.Location(id="pg0--url", refresh=False),
        html.Div(className="layout-database-info", children=Layouts.database_info())
        ])


class Layouts:
    @staticmethod
    def database_info():
        banco_dados = database.BancoDados()
        banco_infos = [
            banco_dados.entregas_tamanho(),
            banco_dados.veiculos_tamanho(),
            banco_dados.motoristas_tamanho()
            ]
        banco_dados.finalizar()

        return [
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-entregas.svg"), width="70px", height="70px"),
                html.H2("Entregas"),
                html.H1(banco_infos[0])
                ]),
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-veiculos.svg"), width="70px", height="70px"),
                html.H2("Veículos"),
                html.H1(banco_infos[1])
                ]),
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-motoristas.svg"), width="70px", height="70px"),
                html.H2("Motoristas"),
                html.H1(banco_infos[2])
                ])
            ]
