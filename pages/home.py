from tkinter.ttk import Style
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
    return html.Div(children=[
        html.Div(id="card--entregas-andamento", children=[
            html.Div(className="box--entrega"),
            html.H1("Entragas em andamento"),
            html.P("Algumas entregas que estaão em andamento no dia"),
            dcc.Dropdown(className="dropdown home--andamento"),
            
        ])
    ])

