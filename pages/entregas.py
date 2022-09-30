from dash import html, dcc, Input, Output, State
from plotly import graph_objects as go
from plotly import express as px

import database
import plugins
import dash

dash.register_page(
    __name__,
    path="/entregas",
    title="Painel de Entregas",
    name="entregas",
    order=1
    )


def layout():
    return html.Div(id="entregas-body", children=[
        html.Div(className="linha", children=[
            html.Div(className="coluna entregas-esquerda", children=[
                html.Div(className="box entregas-pesquisa", children=[
                    html.H1("Entregas"),
                    html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do"
                           "banco de dados."),
                    dcc.Dropdown(className="dropdown", id="entregas-dropdown", value=1, clearable=False),
                    dcc.Checklist(id="entregas-checklist", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                                  value=[True], inline=True)
                    ]),
                html.Div(className="box", children=[
                    html.H1("Informações Gerais"),
                    html.Div(id="entregas-informacoes"),
                    html.Div(className="linha", children=[
                        html.Button(className="botao entregas", id="entregas-botao-entregue", children="Marcar c/ Entregue"),
                        html.Button(className="botao entregas", id="entregas-botao-saida", children="Saiu p/ Entrega")
                        ]),
                    ])
                ]),
            html.Div(className="coluna entregas-rotas", children=[
                html.Div(className="box entregas-rotas", children=[
                    dcc.Graph(id="entregas-mapa"),
                    html.Div(id="entregas-tabela")
                    ]),
                ])
            ])
        ])


@dash.callback(
    [
        Output("entregas-mapa", "figure"),
        Output("entregas-tabela", "children"),
        Output("entregas-informacoes", "children")
    ],
    Input("entregas-dropdown", "value"),
    )
def dropdown_callbacks(id_entrega: int):
    """Atualiza a página de entregas conforme o dropdown."""
    banco_dados = database.BancoDados()
    rotas_entrega = plugins.maps.GoogleMaps(id_entrega)

    def output_mapa(lista_rotas: list[dict]):
        """Retorna um mapa com as diferentes rotas de viagem."""
        mapa = go.Figure()
        for rota in lista_rotas:
            mapa.add_trace(go.Scattermapbox(
                mode="lines"
                ))
        
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
        return [
            html.Div(className="box", style={"margin-top": "15px"}, children=[
                html.H1(f"Rota {rota['index']}"),
                html.Table(className="entregas-tabela", children=[
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
                        ])
                        for parada in rota["paradas"]]
                    ]),
                ])
            for rota in lista_rotas
            ]

    def output_informacoes(banco: database.BancoDados):
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

    return (
        output_mapa(rotas_entrega.rota_dataframe),
        output_rotas(rotas_entrega.rota_organizada),
        output_informacoes(banco_dados)
        )


@dash.callback(
    Output("entregas-dropdown", "options"),
    Input("entregas-checklist", "value")
    )
def filtrar_entregas(filtro: bool):
    """Filtra as entregas já concluídas do dropdown."""
    banco_dados = database.BancoDados()
    opcoes = list()
    for linha in banco_dados.entregas_lista():
        if not filtro and linha[-2] == "Entregue ":
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


@dash.callback(
    Output("none", "children"),
    Input("entregas-botao-entregue", "n_clicks"),
    State("entregas-dropdown", "value"),
    prevent_initial_call=True
    )
def marcar_entregue(_, id_entrega: int):
    return dash.no_update
