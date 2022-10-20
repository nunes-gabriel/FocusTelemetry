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

    def status_veiculo():
        nonlocal em_viagem, id_entrega
        entregas_andamento = banco_dados.entregas_andamento()
        for entrega in entregas_andamento:
            if veiculo[1] == entrega[1]:
                em_viagem = True
                id_entrega = entrega[0]
        else:
            em_viagem = False


def layout_forms():
    return html.Div(className="modal", style={"visibility": "hidden"}, id="pg2--mod0", children=[
        html.Button(className="modal-backdrop",
                    n_clicks=0, id="pg2--mod0-backdrop"),
        html.Div(className="card modal-body", id="pg2--mod0-conteudo", children=[
            html.H1("Registrar Veículo"),
            html.Form(className="modal-form", children=[
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Placa"),
                        dcc.Input(className="input", type="text", maxLength=7, id="pg2--forms-0")])
                    ]),
                html.Div(className="row form-field", children=[
                     html.Label([
                        html.Span("Marca"),
                        dcc.Input(className="input", type="text", id="pg2--forms-1")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span(className="span-dropdown", children="Tipo de Veículo"),
                        dcc.Dropdown(className="form-field dropdown", clearable=False, options=[{"label": "Tração", "value": "Tração"}],
                                     value="Tração", id="pg2--forms-2"),
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span(className="span-datepicker", children="Documentação"),
                        dcc.DatePickerSingle(className="form-field datepicker", placeholder="Data", display_format="DD/MM/YYYY",
                                             id="pg2--forms-3")])
                    ]),
                 html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Cor"),
                        dcc.Input(className="input", type="text", id="pg2--forms-4")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                     html.Label([
                        html.Span("Código Renavam"),
                        dcc.Input(className="input", type="text", pattern=u"[0-9]+", maxLength=11, id="pg2--forms-5")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Ano do Veículo"),
                        dcc.Input(className="input", type="number", min=1980, id="pg2--forms-6")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span(className="span-dropdown", children="Tipo de Carroceria"),
                        dcc.Dropdown(className="form-field dropdown", clearable=False, id="pg2--forms-7", value="Aberta", options=[
                            {"label": "Aberta", "value": "Aberta"},
                            {"label": "Báu Fechado ", "value": "Báu Fechado "},
                            {"label": "Báu Frigorificado", "value": "Báu Frigorificado"},
                            {"label": "Cegonha ", "value": "Cegonha "},
                            {"label": "Granaleira", "value": "Granaleira"},
                            {"label": "Porta-Container", "value": "Porta-Container"},
                            {"label": "Sider", "value": "Sider"},
                            {"label": "Tanque ", "value": "Tanque "}
                            ])
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Altura(m)"),
                        dcc.Input(className="input", type="number", id="pg2--forms-8")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Largura(m)"),
                        dcc.Input(className="input", type="number", id="pg2--forms-9")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Comprimento(m)"),
                        dcc.Input(className="input", type="number", id="pg2--forms-10")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Tara(kg)"),
                        dcc.Input(className="input", type="number", id="pg2--forms-11")
                        ])
                    ]),
                html.Div(className="row form-field", children=[
                    html.Label([
                        html.Span("Capacidade(kg)"),
                        dcc.Input(className="input", type="number", id="pg2--forms-12")
                        ])
                    ])
                ]),
            html.Div(id="pg2--forms-feedback"),
            html.Div(className="row form-buttons", children=[
                html.Button(className="button form-button click", n_clicks=0, id="pg2--mod0-confirmar", children="Confirmar"),
                html.Button(className="button form-button click", n_clicks=0, id="pg2--mod0-cancelar", children="Cancelar")
                ])
            ])
        ])


def layout_cardlist(veiculos=None):
    img_arquivos = listdir("./assets/images/veiculos/")
    img_nomes = [img.split(".")[0] for img in img_arquivos]

    return [
        dcc.Link(style={"text-decoration": "none"}, href=f"/veiculos?placa={veiculo[1]}", refresh=False, children=[
            html.Div(className="card-list-item click", children=[
                html.Img(src=dash.get_asset_url(f"images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
                         width="100px", height="100px")
                if veiculo[1] in img_nomes else
                html.Div(className="no-img", children=html.Img(
                    src=dash.get_asset_url("icons/icone-camera.svg"), width="45px", height="45px"
                    )),
                html.Div(children=[
                    html.P(f"Placa: {veiculo[1]}"),
                    html.P(f"Marca: {veiculo[2]}")
                    ])
                ])
            ])
        for veiculo in veiculos
        ]
    # img = img.removeprefix("data:image/jpeg;base64,")
                # dcc.ConfirmDialogProvider(id="pg2--deletar", message="Tem certeza que deseja deletar o veículo selecionado?", children=html.Button(
                #     n_clicks=0, className="button-infos-B click", children=html.Img(
                #         src=dash.get_asset_url("icons/icone-lixeira.svg"), width="30px", height="30px"
                #         )
                #     )),