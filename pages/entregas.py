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
    return html.Div(children=[
        dcc.Graph(id="entregas--mapa"),
        html.Div(className="card entregas--pesquisa", children=[
            html.H1("Entregas"),
            html.P("Escolha uma entrega para análise ou registre uma nova entrega no banco de dados."),
            dcc.Dropdown(className="dropdown", id="entregas--dropdown", value=1, clearable=False),
            dcc.Checklist(id="entregas--checklist", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                value=[True], inline=True)
            ]),
        html.Div(className="card entregas--informacoes", children=[
            html.H1("Informações"),
            html.Div(id="entregas--informacoes"),
            html.H2("Paradas"),
            html.Table(id="entregas--tabela"),
            html.Button(className="button", id="entregas--botao-entregue", children="Marcar como entregue"),
            html.Br(),
            html.Button(className="button", id="entregas--botao-saida", children="Saiu para entrega")
            ])
        ])


@dash.callback(
    [
        Output("entregas--mapa", "figure"),
        Output("entregas--informacoes", "children"),
        Output("entregas--tabela", "children"),
    ],
    Input("entregas--dropdown", "value"),
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
                mode="lines",
                lon=rota["linhas"]["lon"],
                lat=rota["linhas"]["lat"],
                name=rota["linhas"]["nome"],
                line={
                    "color": "#173C85"
                    }
                ))
        else:
            return mapa.add_trace(go.Scattermapbox(
                mode="markers",
                lon=rota["pontos"]["lon"],
                lat=rota["pontos"]["lat"],
                name="Paradas",
                marker={
                    "size": 8,
                    "color": "#E8E7E7"
                    }
                )) \
            .update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                mapbox={
                    "center": {"lon": -53.1805017, "lat": -14.2400732},
                    "style": "carto-darkmatter",
                    "zoom": 4
                    }
                ) \
            .update_traces(showlegend=False)

    def output_informacoes(banco: database.BancoDados):
        dados = banco.entregas_busca(id_entrega)
        return [
            html.P(f"ID da Entrega: {id_entrega}"),
            html.P(f"Status Atual: {dados[-2]}"),
            html.P(f"Data de Saída: {dados[9]}"),
            html.P(f"Previsão de Entrega: {dados[10]}"),
            html.Hr(),
            html.P(f"Placa do Veículo: {dados[1]}"),
            html.P(f"CPF do Motorista: {dados[2]}"),
            html.P(f"Tipo de Carga: {dados[5]}"),
            html.P(f"Peso da Carga: {dados[6]}kg")
            ]

    def output_tabela(lista_rotas: list[dict]):
        return html.Tbody([
            html.Tr(children=[
                html.Td(className="left", children=f"{parada['index']}ª"),
                html.Td(parada['parada'])
                ])
            for parada in lista_rotas[0]["paradas"]
            ])

    return (
        output_mapa(rotas_entrega.rota_dataframe),
        output_informacoes(banco_dados),
        output_tabela(rotas_entrega.rota_organizada)
        )


@dash.callback(
    Output("entregas--dropdown", "options"),
    Input("entregas--checklist", "value")
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


# @dash.callback(
#     Output("none", "children"),
#     Input("entregas-botao-entregue", "n_clicks"),
#     State("entregas-dropdown", "value"),
#     prevent_initial_call=True
#     )
# def marcar_entregue(_, id_entrega: int):
#     return dash.no_update
