from dash import html, dcc, Input, Output, State
from plotly import express as px
from os import listdir

import database
import dash

from database import banco_dados

dash.register_page(
    __name__,
    path="/veiculos",
    title="Painel de Veículos",
    name="veiculos",
    order=2
    )


def layout(**query):
    return html.Div(children=[
        dcc.Location(id="veiculos--url", refresh=False),
        html.Div(className="card veiculos--pesquisa", children=[
            html.H1("Veículos"),
            html.P("Escolha um veículo para análise e/ou edição ou cadastre um novo veículo no sistema."),
            html.Div(className="row", children=[
                dcc.Dropdown(className="dropdown veiculos--pesquisa", id="veiculos--dropdown", options=_OPTIONS(), value="placa", clearable=False),
                dcc.Input(className="input veiculos--pesquisa", id="veiculos--input", type="search", debounce=False,
                    placeholder="Pesquisar veículo por placa...")
                ]),
            html.Div(id="veiculos--lista", style={"padding-right": "5px"}, children=_LISTA(_BUSCA()))
            ]),
        html.Div(className="card veiculos--informacoes", id="veiculos--informacoes")
        ])


def _OPTIONS():
    return [
        {"label": "Placa", "value": "placa"},
        {"label": "Marca", "value": "marca"},
        {"label": "Cor", "value": "cor"},
        {"label": "Ano", "value": "ano"}
        ]


def _BUSCA(busca=None, filtro=None):
    banco_dados = database.BancoDados()
    veiculos = banco_dados.veiculos_lista()
    if busca not in [None, ""]:
        for index, opcao in enumerate(_OPTIONS()):
            if opcao["value"] == filtro:
                index += 1
                break
        busca = busca.upper()
        veiculos_filtrado = list()
        for veiculo in veiculos:
            if veiculo[index].upper().startswith(busca):
                veiculos_filtrado.append(veiculo)
        veiculos = veiculos_filtrado
    banco_dados.finalizar()
    return veiculos


def _LISTA(veiculos=None):
    img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
    img_arquivos = listdir("./assets/images/veiculos/")

    return [
        dcc.Link(className="card-busca-link", href=f"/veiculos?placa={veiculo[1]}", refresh=False, children=[
            html.Div(className="card-busca", children=[
                html.Img(src=dash.get_asset_url(f"/images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
                    width="120px", height="135px")
                if veiculo[1] in img_nomes else
                html.Div(className="sem-imagem", children=html.Img(
                    src=dash.get_asset_url("/icons/icone-camera.svg"), width="50px", height="50px"
                    )),
                html.Div(children=[
                    html.P(f"Placa: {veiculo[1]}"),
                    html.P(f"Marca: {veiculo[2]}"),
                    html.P(f"Cor: {veiculo[3]}"),
                    html.P(f"Ano: {veiculo[4]}")
                    ])
                ])
            ])
        for veiculo in veiculos
        ]


@dash.callback(
    Output("veiculos--input", "placeholder"),
    Input("veiculos--dropdown", "value"),
    prevent_initial_call=True
    )
def atualizar_placeholder(filtro: str):
    return f"Pesquisar veículo por {filtro}..."

@dash.callback(
    Output("veiculos--lista", "children"),
    Output("veiculos--lista", "style"),
    Input("veiculos--input", "value"),
    State("veiculos--dropdown", "value"),
    prevent_initial_call=True
    )
def filtrar_veiculos(busca: str, filtro: str):
    veiculos = _BUSCA(busca, filtro)

    def lista_children():
        return _LISTA(veiculos)
    
    def lista_style():
        return {"padding-right": "5px"} if len(veiculos) > 3 else {"padding-right": "0"}

    return lista_children(), lista_style()


@dash.callback(
    Output("veiculos--informacoes", "children"),
    Input("veiculos--url", "search")
    )
def informacoes_veiculo(url: str):
    query = dict()
    veiculo = None
    entregas = None
    status = None

    banco_dados = database.BancoDados()
    img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
    img_arquivos = listdir("./assets/images/veiculos/")

    def _QUERY():
        nonlocal query
        for arg in url.split("?")[1:]:
            var, valor = arg.split("=")
            query[var] = valor

    def _VEICULO():
        nonlocal veiculo
        if url == "":
            veiculo = _BUSCA()[0]
        else:
            veiculo = banco_dados.veiculos_busca(query["placa"])

    def _ENTREGA():
        nonlocal entregas
        entregas = banco_dados.veiculos_entregas(veiculo[1])

    def _STATUS():
        nonlocal status
        entregas_andamento = banco_dados.entregas_andamento()
        for entrega in entregas_andamento:
            if veiculo[1] == entrega[1]:
                status = True
        else:
            status = False

    _QUERY()
    _VEICULO()
    _ENTREGA()

    banco_dados.finalizar()

    return [
        html.Img(src=dash.get_asset_url(f"/images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
            width="260px", height="325px")
        if veiculo[1] in img_nomes else
        html.Div(className="sem-imagem veiculos--informacoes", children=html.Img(
            src=dash.get_asset_url("/icons/icone-camera.svg"), width="100px", height="100px"
            )),
        html.Div(className="conteudo", children=[
            html.Div(className="informacoes-basicas", children=[
                html.P(f"Placa: {veiculo[1]}"),
                html.P(f"Marca: {veiculo[2]}"),
                html.P(f"Cor do Veículo: {veiculo[3]}"),
                html.P(f"Ano do Veículo: {veiculo[4]}"),
                html.P(f"Vencimento dos Documentos: {veiculo[5]}"),
                html.P(f"Entregas Realizadas: {len(entregas)}")
                ]),
            html.Div(className="status", children=[
                html.P(style={"color": "red"}, children="Veículo em viagem...")
                if status else
                html.P(style={"color": "green"}, children="Veículo em espera...")
                ])
            ])
        ]
