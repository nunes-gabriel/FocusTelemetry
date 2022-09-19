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


"""
Lista de Callbacks ('index.py')
 | atualizar_pagina
"""
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


"""
Lista de Callbacks ('entregas.py')
| atualizar_entrega
| | output_mapa
| | output_tabela
| | output_infos_geral
| | output_botao
| filtrar entregas
"""
@app.callback(
    [
        Output("box-rotas-mapa", "figure"),
        Output("box-rotas-tabela", "children"),
        Output("box-info-geral-textos", "children"),
        Output("box-info-geral-entregue", "value")
    ],
    Input("box-pesquisa-dropdown", "value"),
    )
def atualizar_entrega(id_entrega: int):
    """Atualiza a página de entregas conforme o dropdown."""
    rotas_entrega = plugins.maps.GoogleMaps(id_entrega)

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
            html.Tr(children=[
                html.Th("Nome"),
                html.Th("Distância"),
                html.Th("Tempo")
            ]),
            *[html.Tr(children=[
                html.Td(rota["nome"]),
                html.Td(f"{rota['distancia'] / 1000}km"),
                html.Td(f"{rota['tempo'] / 60:.2f}min")
            ]) for rota in lista_rotas]
            ]
    
    def output_infos_geral():
        return [
            html.P(f"ID da Entrega: {id_entrega}"),
            html.P(f"Status Atual: "),
            html.P(f"Data de Saída: "),
            html.P(f"Data de Chegada: ")
            ]
    
    def output_botao():
        return str(id_entrega)

    return output_mapa(rotas_entrega.filtro_dataframe), \
           output_tabela(rotas_entrega.filtro_ordenadas), \
           output_infos_geral(), \
           output_botao()


@app.callback(
    Output("box-pesquisa-dropdown", "options"),
    Input("box-pesquisa-filtro", "value")
    )
def filtrar_entregas(filtro: bool):
    """Filtra as entregas já concluídas do dropdown."""
    if filtro:
        return layouts.entregas_opcoes()
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
