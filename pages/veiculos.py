from dash import html, dcc, Input, Output, State
from os import listdir

import dash_bootstrap_components as dbc
import database
import dash

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
                dcc.Dropdown(className="dropdown veiculos--pesquisa", id="veiculos--dropdown", options=dropdown_options(),
                             value="placa", clearable=False),
                dcc.Input(className="input veiculos--pesquisa", id="veiculos--input", type="search", debounce=False,
                          placeholder="Pesquisar veículo por placa...")
                ]),
            html.Div(id="veiculos--lista", style={"padding-right": "5px"}, children=listar_veiculos(filtro_busca()))
            ]),
        html.Div(className="card veiculos--informacoes", id="veiculos--informacoes")
        ])


def dropdown_options():
    return [
        {"label": "Placa", "value": "placa"},
        {"label": "Marca", "value": "marca"}
        ]


def filtro_busca(busca=None, filtro=None):
    banco_dados = database.BancoDados()
    veiculos = banco_dados.veiculos_lista()
    if busca not in [None, ""]:
        for index, opcao in enumerate(dropdown_options()):
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


def listar_veiculos(veiculos=None):
    img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
    img_arquivos = listdir("./assets/images/veiculos/")

    return [
        dcc.Link(className="card-busca-link", href=f"/veiculos?placa={veiculo[1]}", refresh=False, children=[
            html.Div(className="card-busca", children=[
                html.Img(src=dash.get_asset_url(f"images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
                         width="100px", height="100px")
                if veiculo[1] in img_nomes else
                html.Div(className="sem-imagem", children=html.Img(
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


def veiculo_informacoes(query: str):
    if query == "":
        veiculo = filtro_busca()[0]
    else:
        placa = query.split("?")[1].split("=")[1]
        banco_dados = database.BancoDados()
        veiculo = banco_dados.veiculos_busca(placa)
        banco_dados.finalizar()
    return veiculo


@dash.callback(
    Output("veiculos--input", "placeholder"),
    Input("veiculos--dropdown", "value"),
    prevent_initial_call=True
    )
def _placeholder(filtro: str):
    return f"Pesquisar veículo por {filtro}..."

@dash.callback(
    Output("veiculos--lista", "children"),
    Output("veiculos--lista", "style"),
    Input("veiculos--input", "value"),
    State("veiculos--dropdown", "value"),
    prevent_initial_call=True
    )
def _busca(busca: str, filtro: str):
    veiculos = filtro_busca(busca, filtro)

    def lista_children():
        return listar_veiculos(veiculos)
    
    def lista_style():
        return {"padding-right": "5px"} if len(veiculos) > 4 else {"padding-right": "0"}

    return lista_children(), lista_style()


@dash.callback(
    Output("veiculos--informacoes", "children"),
    Input("veiculos--url", "search")
    )
def _informacoes(url: str):
    em_viagem = None
    id_entrega = None

    veiculo = veiculo_informacoes(url)

    banco_dados = database.BancoDados()

    img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
    img_arquivos = listdir("./assets/images/veiculos/")

    def status_veiculo():
        nonlocal em_viagem, id_entrega
        entregas_andamento = banco_dados.entregas_andamento()
        for entrega in entregas_andamento:
            if veiculo[1] == entrega[1]:
                em_viagem = True
                id_entrega = entrega[0]
        else:
            em_viagem = False

    status_veiculo()

    banco_dados.finalizar()

    return [
        html.Img(className="imagem-informacoes", src=dash.get_asset_url(f"images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
                 width="260px", height="325px")
        if veiculo[1] in img_nomes else
        html.Div(className="sem-imagem veiculos--informacoes", children=html.Img(
            src=dash.get_asset_url("icons/icone-camera.svg"), width="100px", height="100px"
            )),
        html.Div(className="conteudo", children=[
            html.Div(className="informacoes-basicas", children=[
                html.P(f"Placa: {veiculo[1]}"),
                html.P(f"Marca: {veiculo[2]}"),
                html.P(f"Cor do Veículo: {veiculo[3]}"),
                html.P(f"Ano do Veículo: {veiculo[4]}"),
                html.P(f"Vencimento dos Documentos: {veiculo[5]}")
                ]),
            html.Div(className="status", children=[
                dcc.Link(href=f"/entregas?id={id_entrega}", children="Veículo em viagem...")
                if em_viagem else
                html.P(children="Veículo em espera...")
                ])
            ]),
        html.Div(className="botoes", children=[
            dcc.ConfirmDialogProvider(id="veiculos--deletar", message="Tem certeza que deseja deletar o veículo selecionado?", children=html.Button(
                className="botao-informacoes", children=html.Img(
                    src=dash.get_asset_url("icons/icone-lixeira.svg"), width="30px", height="30px"
                    )
                )),
            html.Button(className="botao-informacoes", children=html.Img(
                src=dash.get_asset_url("icons/icone-editar.svg"), width="30px", height="30px"
                ))
            ]),
        ]


@dash.callback(
    Output("veiculos--url", "refresh"),
    Output("veiculos--url", "pathname"),
    Output("veiculos--url", "search"),
    Input("veiculos--deletar", "submit_n_clicks"),
    State("veiculos--url", "pathname"),
    State("veiculos--url", "search"),
    prevent_initial_call=True
    )
def _deletar(submit, path, query):
    if not submit:
        return dash.no_update
    else:
        banco_dados = database.BancoDados()
        veiculo = veiculo_informacoes(query=query)
        banco_dados.veiculos_deletar(veiculo[1])
        banco_dados.finalizar()
        if path == "/veiculos/":
            return True, "/veiculos", ""
        else:
            return True, "/veiculos/", ""
