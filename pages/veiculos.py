from dash import html, dcc, Input, Output, State
from plotly import express as px

import database
import plugins
import dash

dash.register_page(
    __name__,
    path="/veiculos",
    title="Painel de Veículos",
    name="veiculos",
    order=2
    )


def layout():
    return html.Div("Veículos")
