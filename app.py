from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from plotly import express as px

import layouts
import database
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


@app.callback(
    [
        Output("box-rotas-mapa", "figure"),
        Output("box-rotas-tabelas", "children"),
        Output("box-info-geral-textos", "children"),
        Output("box-info-geral-entregue", "value")
    ],
    Input("box-pesquisa-dropdown", "value"),
    )
def atualizar_entrega(id_entrega: int):
    """Atualiza a página de entregas conforme o dropdown."""
    banco_dados = database.BancoDados()
    rotas_entrega = plugins.maps.GoogleMaps(id_entrega)

    def output_mapa(lista_rotas: list[dict]):
        """Retorna um mapa com as diferentes rotas de viagem."""
        return px.line_mapbox(
            data_frame=lista_rotas,
            lat="Latitude",
            lon="Longitude",
            color="Rota",
            zoom=6
            ) \
            .update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
            )

    def output_rotas(lista_rotas: list[dict]):
        """Retorna uma tabela com informações sobre as rotas de viagem."""
        layout_rotas = list()
        for index, rota in enumerate(lista_rotas):
            layout_rotas.extend([
                html.H1(f"Rota {rota['index']}"),
                html.Table(className="box-rotas-tabela", children=[
                    html.Tr(children=[
                        html.Th("Ordem Parada"),
                        html.Th("Endereço"),
                        html.Th("Distância"),
                        html.Th("Duração")
                        ]),
                    * [html.Tr(children=[
                        html.Td(parada["index"]),
                        html.Td(parada["parada"]),
                        html.Td(parada["distância"]),
                        html.Td(parada["duração"])
                        ]) for parada in rota["paradas"]]
                    ]),
                ])
            if index != len(lista_rotas) - 1:
                layout_rotas.append(html.Hr())
        return layout_rotas

    def output_infos_geral(banco: database.BancoDados):
        dados = banco.entregas_busca(id_entrega)
        return [
            html.P([html.Strong("ID da Entrega: "), id_entrega]),
            html.P([html.Strong("Status Atual: "), dados[-2]]),
            html.P([html.Strong("Feedback: "), dados[-1]]),
            html.P([html.Strong("Placa do Veículo: "), dados[1]]),
            html.P([html.Strong("CPF do Motorista: "), dados[2]]),
            html.P([html.Strong("Data de Saída: "), dados[9]]),
            html.P([html.Strong("Data Prevista: "), dados[10]]),
            html.P([html.Strong("Data de Chegada: "), dados[11]]),
            html.P([html.Strong("Tipo de Carga: "), dados[5]]),
            html.P([html.Strong("Peso da Carga: "), dados[6], "kg"]),
            html.P([html.Strong("Valor da Carga: "), "R$", dados[7]]),
            html.P([html.Strong("Número de Paradas: "), dados[8].split("/").__len__() + 1])
            ]

    def output_botao():
        return str(id_entrega)

    return (
        output_mapa(rotas_entrega.rota_dataframe),
        output_rotas(rotas_entrega.rota_organizada),
        output_infos_geral(banco_dados),
        output_botao()
        )


@app.callback(
    Output("box-pesquisa-dropdown", "options"),
    Input("box-pesquisa-filtro", "value")
    )
def filtrar_entregas(filtro: bool):
    """Filtra as entregas já concluídas do dropdown."""
    if filtro:
        return layouts.entregas_opcoes()
    else:
        banco_dados = database.BancoDados()
        opcoes = list()
        for linha in banco_dados.entregas_lista():
            if linha[-2] == "Entregue ":
                continue
            label_meio = "//"
            if linha[8] != "Sem parada ":
                paradas = linha[8].split("/")
                if len(paradas) > 2:
                    label_meio += f" {paradas[0]} // ... // {paradas[-1]}  //"
                else:
                    for parada in paradas:
                        label_meio += f" {parada} //"
            opcoes.append({
                "label": f"ID#{linha[0]} - {linha[3]} {label_meio} {linha[4]}",
                "value": linha[0]
            })
        else:
            banco_dados.finalizar()
            return opcoes


@app.callback(
    Output("no_update", "children"),
    Input("box-info-geral-entregue", "n_clicks"),
    State("box-pesquisa-dropdown", "value"),
    prevent_initial_call=True
    )
def marcar_entregue(_, id_entrega: int):
    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
