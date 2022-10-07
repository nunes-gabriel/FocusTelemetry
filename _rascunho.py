    # if busca in [None, ""]:
    #     filtro = None
    # else:
    #     for index, opcao in enumerate(_options()):
    #         if opcao["value"] == filtro:
    #             index += 1
    #             break
    #     busca = busca.upper()
    # banco_dados = database.BancoDados()
    # veiculos: list[tuple[str]] = banco_dados.veiculos_lista()
    # if filtro is not None:
    #     veiculos_filtrado = list()
    #     for veiculo in veiculos:
    #         if veiculo[index].upper().startswith(busca):
    #             veiculos_filtrado.append(veiculo)
    #     veiculos = veiculos_filtrado
    # banco_dados.finalizar()
    # imagens_nomes = [imagem.split(".")[0] for imagem in listdir("./assets/images/veiculos/")]
    # imagens_arquivos = listdir("./assets/images/veiculos/")


from dash import html, dcc, Input, Output, State
from plotly import graph_objects as go

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
        html.Div(id="entregas--mapa-fadeout"),
        html.Div(className="card entregas--pesquisa", children=[
            html.H1("Entregas"),
            html.P("Escolha uma entrega para análise ou cadastre uma nova entrega no sistema."),
            dcc.Dropdown(className="dropdown entregas--pesquisa", id="entregas--dropdown", value=1, clearable=False),
            dcc.Checklist(className="checklist entregas--pesquisa", id="entregas--checklist", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                value=[True], inline=True)
            ]),
        html.Div(className="card entregas--informacoes", children=[
            html.H1("Informações"),
            html.Div(id="entregas--informacoes"),
            html.H2("Paradas"),
            html.Table(id="entregas--tabela"),
            html.Button(className="botao entregas--informacoes", id="entregas--botao-entregue", children="Marcar como entregue"),
            html.Br(),
            html.Button(className="botao entregas--informacoes", id="entregas--botao-saida", children="Saiu para entrega")
            ]),
        html.Div(id="entregas--legenda", children=[
            html.Label([html.Span(className="circulo ponto--partida"), "Ponto de Partida"]),
            html.Label([html.Span(className="circulo ponto--parada"), "Ponto de Parada"]),
            html.Label([html.Hr(className="linha rota--recomendada"), "Rota Recomendada"]),
            html.Label([html.Hr(className="linha rota--alternativas"), "Rota Alternativa"])
            ])
        ])


@dash.callback(
    Output("entregas--mapa", "figure"),
    Output("entregas--informacoes", "children"),
    Output("entregas--tabela", "children"),
    Input("entregas--dropdown", "value"),
    )
def dropdown_callbacks(id_entrega: int):
    maps = plugins.maps.GoogleMaps(id_entrega)

    banco_dados = database.BancoDados()
    dados_entrega = banco_dados.entregas_busca(id_entrega)
    banco_dados.finalizar()

    def mapa_figure():
        mapa = go.Figure()
        for index, rota in enumerate(reversed(maps.rota_dataframe)):
            mapa.add_trace(go.Scattermapbox(
                mode="lines",
                lon=rota["linhas"]["lon"],
                lat=rota["linhas"]["lat"],
                name=rota["linhas"]["nome"],
                hoverinfo="skip",
                line={
                    "color": "#173C85" if index != len(maps.rota_dataframe) - 1 else "red",
                    "width": 3
                    }
                ))
        else:
            return mapa.add_trace(go.Scattermapbox(
                mode="markers",
                lon=rota["pontos"]["lon"],
                lat=rota["pontos"]["lat"],
                name="Parada",
                marker={
                    "size": 11,
                    "color": "#FDF508"
                    }
                )) \
            .add_trace(go.Scattermapbox(
                mode="markers",
                lon=[rota["pontos"]["partida"]["lon"]],
                lat=[rota["pontos"]["partida"]["lat"]],
                name="Partida",
                marker={
                    "size": 11,
                    "color": "#F1F1F1"
                }
                )) \
            .update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                mapbox={
                    "center": {"lon": -53.1805017, "lat": -14.2400732},
                    "style": "carto-darkmatter",
                    "zoom": 4
                    },
                paper_bgcolor="#262626"
                ) \
            .update_traces(showlegend=False)

    def informacoes_children():
        return [
            html.P(f"ID da Entrega: {id_entrega}"),
            html.P(f"Status Atual: {dados_entrega[-2]}"),
            html.P(f"Data de Saída: {dados_entrega[9]}"),
            html.P(f"Previsão de Entrega: {dados_entrega[10]}"),
            html.Hr(),
            html.P(children=[
                "Placa do Veículo: ",
                dcc.Link(href=f"/veiculos/{dados_entrega[1]}", children=dados_entrega[1])
                ]),
            html.P(children=[
                "CPF do Motorista: ",
                dcc.Link(href=f"/motoristas/{dados_entrega[2]}", children=dados_entrega[2])
                ]),
            html.P(f"Tipo de Carga: {dados_entrega[5]}"),
            html.P(f"Peso da Carga: {dados_entrega[6]}kg")
            ]

    def tabela_children():
        return html.Tbody([
            html.Tr(children=[
                html.Td(className="left", children=f"{parada['index']}ª"),
                html.Td(parada['parada'])
                ])
            for parada in maps.rota_organizada[0]["paradas"]
            ])

    return mapa_figure(), informacoes_children(), tabela_children()


@dash.callback(
    Output("entregas--dropdown", "options"),
    Input("entregas--checklist", "value")
    )
def filtrar_entregas(filtro: bool):
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

import locale
from dash import html, dcc, Input, Output, State
from plotly import express as px
from os import listdir

import database
import dash

dash.register_page(
    __name__,
    path="/veiculos",
    path_template="/veiculos/<placa_veiculo>",
    title="Painel de Veículos",
    name="veiculos",
    order=2
    )


def layout(placa_veiculo=None):
    return html.Div(children=[
        html.Div(className="card veiculos--pesquisa", children=[
            html.H1("Veículos"),
            html.P("Escolha um veículo para análise e/ou edição ou cadastre um novo veículo no sistema."),
            html.Div(className="row", children=[
                dcc.Dropdown(className="dropdown veiculos--pesquisa", id="veiculos--dropdown", options=_options(), value="placa", clearable=False),
                dcc.Input(className="input veiculos--pesquisa", id="veiculos--input", type="search", debounce=False)
                ]),
            html.Div(id="veiculos--lista")
            ]),
        html.Div(className="card veiculos--informacoes", children=[
            html.P(id="teste")
            ])
        ])


def _options():
    return [
        {"label": "Placa", "value": "placa"},
        {"label": "Marca", "value": "marca"},
        {"label": "Cor", "value": "cor"},
        {"label": "Ano", "value": "ano"}
        ]


@dash.callback(
    Output("veiculos--input", "placeholder"),
    Input("veiculos--dropdown", "value")
    )
def input_placeholder(filtro: str):
    return f"Pesquisar por {filtro} de veículo..."

@dash.callback(
    Output("veiculos--lista", "children"),
    Output("veiculos--lista", "style"),
    Input("veiculos--input", "value"),
    State("veiculos--dropdown", "value")
    )
def filtrar_veiculos(busca: str, filtro: str):
    veiculos = None
    index = None

    banco_dados = database.BancoDados()
    img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
    img_arquivos = listdir("./assets/images/veiculos/")

    def _FILTRO():
        nonlocal busca, filtro
        if busca in [None, ""]:
            filtro = None
        else:
            nonlocal index
            for index, opcao in enumerate(_options()):
                if opcao["value"] == filtro:
                    index += 1
                    break
            busca = busca.upper()

    def _BUSCA():
        nonlocal veiculos
        veiculos = banco_dados.veiculos_lista()
        if filtro is not None:
            veiculos_filtrado = list()
            for veiculo in veiculos:
                if veiculo[index].upper().startswith(busca):
                    veiculos_filtrado.append(veiculo)
            veiculos = veiculos_filtrado

    def lista_children():
        return [
            html.Div(className="card-busca", children=[
                html.Img(src=f"./assets/images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}",
                    width="120px", height="135px")
                if veiculo[1] in img_nomes else
                html.Div(className="sem-imagem", children=html.Img(
                    src=f"./assets/icons/icone-camera.svg", width="50px", height="50px"
                    )),
                html.Div(children=[
                    html.P(f"Placa: {veiculo[1]}"),
                    html.P(f"Marca: {veiculo[2]}"),
                    html.P(f"Cor: {veiculo[3]}"),
                    html.P(f"Ano: {veiculo[4]}")
                    ])
                ])
            for veiculo in veiculos
            ]
    
    def lista_style():
        return {"padding-right": "5px"} if len(veiculos) > 3 else {"padding-right": "0"}

    _FILTRO()
    _BUSCA()

    return lista_children(), lista_style()
