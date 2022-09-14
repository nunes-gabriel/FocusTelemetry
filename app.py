from dash import Dash, html, dcc, Input, Output
from plotly import express as px

import layouts
import plugins

app = Dash(__name__, title="Dash - Entra21", update_title="Carregando...")

all_layouts = {
    "index": layouts.index(),
    "home": layouts.home(),
    "entregas": layouts.entregas(),
    "veiculos": layouts.veiculos(),
    "motoristas": layouts.motoristas(),
    "analise": layouts.analise(),
    "banco-dados": layouts.banco_dados(),
    }

app.layout = all_layouts["index"]
app.validation_layout = html.Div([*all_layouts.values()])


@app.callback(
    Output("conteudo-pagina", "children"),
    Input("url", "pathname")
    )
def alterar_painel(pathname: str):
    """
    Navega entre os diferentes paineis do Dashboard através de uma barra lateral
    que alterna o caminho URL da página executando o callback.
    """
    if pathname == "/entregas":
        return all_layouts["entregas"]
    elif pathname == "/veiculos":
        return all_layouts["veiculos"]
    elif pathname == "/motoristas":
        return all_layouts["motoristas"]
    elif pathname == "/analise":
        return all_layouts["analise"]
    elif pathname == "/banco-dados":
        return all_layouts["banco-dados"]
    else:
        return all_layouts["home"]


@app.callback(
    [
        Output("entregas-mapa", "figure"),
        Output("entregas-tabela-rotas", "children")
    ],
    Input("entregas-dropdown", "value")
    )
def atualizar_mapa(entrega: str):
    entrega = entrega.split(" - ")
    rotas = plugins.maps.GoogleMaps(
        int(entrega[0].removeprefix("COD#")),
        entrega[1].split(" / ")[0],
        entrega[1].split(" / ")[-1]
        )

    def gerar_mapa(data: list[dict]):
        figure_mapa = px.line_mapbox(
            data_frame=data,
            lat="latitude",
            lon="longitude",
            color="nome",
            zoom=11
            )
        figure_mapa.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
            )
        return figure_mapa

    def gerar_tabela(data: list[dict]):
        tabela = [
            html.Tr(className="cabecalho", children=[
                html.Th("Nome"), html.Th("Distância"), html.Th("Tempo")
                ])
            ]
        for rota in data:
            tabela.append(
                html.Tr([
                    html.Th(rota["nome"]),
                    html.Th(f"{rota['distancia'] / 1000}km"),
                    html.Th(f"{rota['tempo'] / 60:.2f}min")
                    ])
                )
        return tabela
    
    return gerar_mapa(rotas.data_frame), gerar_tabela(rotas.dicionario)


if __name__ == "__main__":
    app.run_server(debug=True)
