from dash import html, dcc, Input, Output, State
from plotly import express as px

import database
import plugins
import dash

dash.register_page(
    __name__,
    path="/banco-dados",
    title="Painel do Banco de Dados",
    name="banco-dados",
    order=4
    )


def layout():
    return html.Div("Banco de Dados")
