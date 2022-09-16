from dash import Dash, html, dcc, Input, Output, State
from plotly import express as px
from pandas import read_csv

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


# Callbacks -> 'index.py'
@app.callback(
    Output("conteudo-pagina", "children"),
    Input("url", "pathname")
)
def atualizar_pagina(pathname: str):
    """Atualiza o layout da página conforme o URL."""
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


# Callbacks -> 'entregas.py'
@app.callback(
    [
        Output("entregas-mapa", "figure"),
        Output("entregas-tabela-rotas", "children")
    ],
    Input("entregas-dropdown", "value"),
)
def atualizar_entrega(id_entrega: int):
    """Atualiza a página de entregas conforme o dropdown."""
    rotas = plugins.maps.GoogleMaps(id_entrega)

    def output_mapa(lista_rotas: list[dict]):
        """Retorna um mapa com as diferentes rotas de viagem."""
        return px.line_mapbox(
            data_frame=lista_rotas,
            lat="latitude",
            lon="longitude",
            color="nome",
            zoom=11
        ) \
            .update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

    def output_tabela(lista_rotas: list[dict]):
        """Retorna uma tabela com informações sobre as rotas de viagem."""
        return [
            html.Tr(className="cabecalho", children=[
                html.Th("Nome"),
                html.Th("Distância"),
                html.Th("Tempo")
            ]),
            *[html.Tr([
                html.Th(rota["nome"]),
                html.Th(f"{rota['distancia'] / 1000}km"),
                html.Th(f"{rota['tempo'] / 60:.2f}min")
            ]) for rota in lista_rotas]
        ]

    return output_mapa(rotas.filtro_dataframe), output_tabela(rotas.filtro_ordenadas)


@app.callback(
    Output("entregas-dropdown", "options"),
    Input("entregas-filtro", "value")
    )
def filtrar_entregas(filtro: bool):
    """Filtra as entregas já concluídas do dropdown."""
    if filtro:
        return layouts.options()
    else:
        dados = read_csv("./database/_dataframe.csv", delimiter=";")
        lista_opcoes = list()
        for linha in dados.iterrows():
            linha = dict(linha[1])
            if linha["em_viagem"]:
                lista_opcoes.append({
                    "label": f"COD#{linha['id']} - {linha['ponto_partida']} // {linha['ponto_chegada']}",
                    "value": linha["id"]
                    })
        return lista_opcoes


if __name__ == "__main__":
    app.run_server(debug=True)
