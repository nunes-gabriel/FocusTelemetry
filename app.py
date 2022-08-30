# --> Módulos e Bibliotecas
from dash import Dash, html, dcc, Input, Output
from pages.index import index
from pages.entregas import entregas


# --> App e Meta
app = Dash(__name__, title="Dash - Entra", use_pages=False)


# --> Layouts de Páginas
url_getter = html.Div([dcc.Location(id="url", refresh=False), html.Div(id="conteudo-pagina")])

layouts = {
    "page-index": index(),
    "page-entregas": entregas(),
    }

app.layout = url_getter

app.validation_layout = html.Div([
    url_getter, *layouts.values()
    ])


# --> Funções e Callbacks
@app.callback(Output("conteudo-pagina", "children"), Input("url", "pathname"))
def alterar_pagina(pathname: str):
    if pathname == "/entregas":
        return layouts["page-entregas"]
    else:
        return layouts["page-index"]


# --> Run Server
if __name__ == "__main__":
    app.run_server(debug=True)
