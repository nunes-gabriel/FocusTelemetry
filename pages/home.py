from dash import html, dcc, Input, Output, State
from plotly import express as px

import database
import plugins
import dash

dash.register_page(
    __name__,
    path="/",
    title="Home",
    name="home",
    order=0
    )


def layout():
    return html.Div("Home")
