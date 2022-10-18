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
            html.Div(className="row veiculos--pesquisa", children=[
                dcc.Dropdown(className="dropdown veiculos--pesquisa", id="veiculos--dropdown", options=dropdown_options(),
                             value="placa", clearable=False),
                dcc.Input(className="input veiculos--pesquisa", id="veiculos--input", type="search", debounce=False,
                          placeholder="Pesquisar veículo por placa..."),
                html.Button(className="botao-modal-abrir", n_clicks=0, id="veiculos--modal-abrir-novo", children=html.Img(
                    src=dash.get_asset_url("icons/icone-adicionar.svg"), width="32px", height="32px"
                    ))
                ]),
            html.Div(id="veiculos--lista", style={"padding-right": "5px"}, children=listar_veiculos(filtro_busca()))
            ]),
        html.Div(className="card veiculos--informacoes", id="veiculos--informacoes"),
        html.Div(className="modal", style={"visibility": "hidden"}, id="veiculos--modal", children=[
            html.Button(className="backdrop", n_clicks=0, id="veiculos--modal-backdrop"),
            html.Div(className="modal-conteudo card", id="veiculos--modal-conteudo", children=[
                html.Button(className="botao-modal-fechar", n_clicks=0, id="veiculos--modal-fechar", children=html.Img(
                    src=dash.get_asset_url("icons/icone-fechar.svg"), width="30px", height="30px"
                    )),
                html.H1("Registrar Veículo"),
                html.Div(className="inputs", children=[
                    html.Label([
                        "Placa: ",
                        dcc.Input(className="input cadastro", type="text", maxLength=8, id="veiculos--cadastro-placa")
                        ]),
                    html.Label([
                        "Marca: ",
                        dcc.Input(className="input cadastro", type="text", id="veiculos--cadastro-marca")
                        ]),
                    html.Label([
                        "Tipo de Veículo: ",
                        dcc.Dropdown(className="dropdown cadastro", options=[{"label": "Tração", "value": "Tração"}], value="Tração",
                                     id="veiculos--cadastro-tipo-veiculo")
                        ]),
                    html.Label([
                        "Cor: ",
                        dcc.Input(className="input cadastro", type="text", id="veiculos--cadastro-cor")
                        ]),
                    html.Label([
                        "RENAVAM: ",
                        dcc.Input(className="input cadastro", type="text", pattern=u"[0-9]+", maxLength=11, id="veiculos--cadastro-renavam")
                        ]),
                    html.Label([
                        "Ano: ",
                        dcc.Input(className="input cadastro", type="number", min=1980, id="veiculos--cadastro-ano")
                        ]),
                    html.Label([
                        "Tipo de Carroceria: ",
                        dcc.Dropdown(className="dropdown cadastro", id="veiculos--cadastro-tipo-carroceria", value="Aberta", options=[
                            {"label": "Aberta", "value": "Aberta"},
                            {"label": "Báu Fechado ", "value": "Báu Fechado "},
                            {"label": "Báu Frigorificado", "value": "Báu Frigorificado"},
                            {"label": "Cegonha ", "value": "Cegonha "},
                            {"label": "Granaleira", "value": "Granaleira"},
                            {"label": "Porta-Container", "value": "Porta-Container"},
                            {"label": "Sider", "value": "Sider"},
                            {"label": "Tanque ", "value": "Tanque "}
                            ])
                        ]),
                    ])
                ])
            ]),
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
def placeholder(filtro: str):
    return f"Pesquisar veículo por {filtro}..."

@dash.callback(
    Output("veiculos--lista", "children"),
    Output("veiculos--lista", "style"),
    Input("veiculos--input", "value"),
    State("veiculos--dropdown", "value"),
    prevent_initial_call=True
    )
def busca(busca: str, filtro: str):
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
def informacoes(url: str):
    em_viagem = None
    id_entrega = None

    veiculo = veiculo_informacoes(url)

    banco_dados = database.BancoDados()

    img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
    img_arquivos = listdir("./assets/images/veiculos/")

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
                html.P(f"Cor: {veiculo[4]}"),
                html.P(f"Tipo de Veículo: {veiculo[3]}"),
                html.P(f"Tipo de Carroceria: {veiculo[7]}"),
                html.P(f"RENAVAM: {veiculo[5]}"),
                html.P(f"Ano: {veiculo[6]}"),
                html.P(f"Altura: {float(veiculo[8]):.2f}m")
                ]),
            html.Div(className="status", children=[
                dcc.Link(href=f"/entregas?id={id_entrega}", children="Veículo em viagem...")
                if veiculo[-1] == "Em Viagem " else
                html.P(children=f"Veículo {veiculo[-1].strip().lower()}...")
                ])
            ]),
        html.Div(className="botoes", children=[
            dcc.ConfirmDialogProvider(id="veiculos--deletar", message="Tem certeza que deseja deletar o veículo selecionado?", children=html.Button(
                n_clicks=0, className="botao-informacoes deletar", children=html.Img(
                    src=dash.get_asset_url("icons/icone-lixeira.svg"), width="30px", height="30px"
                    )
                )),
            html.Button(className="botao-informacoes", n_clicks=0, id="veiculos--modal-abrir-edicao", children=html.Img(
                src=dash.get_asset_url("icons/icone-editar.svg"), width="30px", height="30px"
                ))
            ])
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
def deletar(submit, path, query):
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


@dash.callback(
    Output("veiculos--modal", "style"),
    Input("veiculos--modal-abrir-novo", "n_clicks"),
    Input("veiculos--modal-abrir-edicao", "n_clicks"),
    Input("veiculos--modal-backdrop", "n_clicks"),
    Input("veiculos--modal-fechar", "n_clicks"), 
    State("veiculos--modal", "style"),
    prevent_initial_call=True
    )
def abrir_modal(b1, b2, b3, b4, modal):
    if b1 or b2 or b3 or b4:
        if modal["visibility"] == "hidden":
            return {"visibility": "visible"}
        else:
            return {"visibility": "hidden"}
    else:
        return dash.no_update
