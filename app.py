# --> Módulos e Bibliotecas
from dash import Dash, html, dcc, Input, Output
from layouts.index import index
from layouts.entregas import entregas


# --> App e Meta
app = Dash(__name__, title="Dash - Entra21", use_pages=False)


# --> Layouts de Páginas
layouts = {
    "page-index": index(),
    "page-entregas": entregas(),
    }

app.layout = layouts["page-index"]

app.validation_layout = html.Div([*layouts.values()])


# --> Funções e Callbacks
@app.callback(Output("conteudo-pagina", "children"), Input("url", "pathname"))
def alterar_pagina(pathname: str):
    if pathname == "/entregas":
        return layouts["page-entregas"]
    else:
        return layouts["page-entregas"]


# --> Run Server
if __name__ == "__main__":
    app.run_server(debug=True)
