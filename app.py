from dash import Dash, html, Input, Output
from layouts.index import index_layout
from layouts.entregas import entregas_layout
from layouts.veiculos import veiculos_layout
from layouts.motoristas import motoristas_layout
from layouts.analise import analise_layout
from layouts.banco_dados import banco_dados_layout
from testes.layouts import entregas


app = Dash(__name__, title="Dash - Entra21", update_title="Carregando...")


layouts = {
    "index": index_layout(),
    "entregas": entregas_layout(),
    "veiculos": veiculos_layout(),
    "motoristas": motoristas_layout(),
    "analise": analise_layout(),
    "banco-dados": banco_dados_layout(),
    }


app.layout = layouts["index"]
app.validation_layout = html.Div([*layouts.values()])


# Callbacks - Index
@app.callback(
    Output("conteudo-pagina", "children"),
    Input("url", "pathname")
    )
def alterar_painel(pathname):
    """
    Navega entre os diferentes paineis do Dashboard através de uma barra lateral
    que alterna o caminho URL da página executando o callback.
    """
    if pathname == "/veiculos":
        return layouts["veiculos"]
    elif pathname == "/motoristas":
        return layouts["motoristas"]
    elif pathname == "/analise":
        return layouts["analise"]
    elif pathname == "/banco-dados":
        return layouts["banco-dados"]
    else:
        return layouts["entregas"]


# Callbacks - Entregas
@app.callback(
    Output("mapa-entregas", "figure"),
    Input("dropdown-entregas", "value"),
    prevent_initial_call=True
    )
def atualizar_mapa(id_entrega):
    """
    Atualiza as rotas de viagem do mapa de acordo com a entrega selecionada no Dropdown
    do painel - exibindo tanto a rota principal quanto as rotas alternativas.
    """
    pass


if __name__ == "__main__":
    app.run_server(debug=True)
