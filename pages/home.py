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
            html.H1("Entragas em andamento"),
            html.P("Algumas entregas que estão em andamento no dia"),
            dcc.Dropdown(className="dropdown home--andamento"),
            html.Button(className="botao criar-entrega", id="home--criar-entrega", children="Nova Entrega")
        ]),
        html.Div(className="card info--geral", children=[
            html.H1("Informações"),
            html.Div(id="entregas--informacoes"),
            html.H2("Paradas"),
            html.Table(id="entregas--tabela"),
        ]),
    ])

