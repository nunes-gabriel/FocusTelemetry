from dash import html, dcc, Input, Output, State
from plotly import express as px

import database
import plugins
import dash

dash.register_page(
    __name__,
    path="/motoristas",
    title="Painel de Motoristas",
    name="motoristas",
    order=3
    )


def layout():
    return html.Div("Motoristas")
