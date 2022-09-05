from dash import Dash, html, Input, Output
from layouts.index import index_layout
from layouts.entregas import entregas_layout


app = Dash(__name__, title="Dash - Entra21", update_title="Carregando...")


layouts = {
    "index": index_layout(),
    "entregas": entregas_layout(),
    }


app.layout = layouts["index"]
app.validation_layout = html.Div([*layouts.values()])


@app.callback(Output("conteudo-pagina", "children"), Input("url", "pathname"))
def alterar_pagina(pathname: str):
    """
    Navega entre os diferentes paineis do Dashboard através de uma barra lateral
    que alterna o caminho URL da página executando o callback.
    """ 
    if pathname == "/entregas":
        return layouts["entregas"]
    else:
        return layouts["entregas"]


if __name__ == "__main__":
    app.run_server(debug=True)
