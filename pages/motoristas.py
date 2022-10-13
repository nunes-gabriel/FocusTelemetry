from dash import html, dcc, Input, Output, State
from os import listdir

import database
import dash

dash.register_page(
    __name__,
    path="/motoristas",
    title="Painel de Motoristas",
    name="motoristas",
    order=3
    )


def layout(**query):
    return html.Div(children=[
        dcc.Location(id="motoristas--url", refresh=False),
        html.Div(className="card veiculos--pesquisa", children=[
            html.H1("Motoristas"),
            html.P("Escolha um motorista para análise e/ou edição ou cadastre um novo motorista no sistema."),
            html.Div(className="row", children=[
                dcc.Dropdown(className="dropdown veiculos--pesquisa", id="veiculos--dropdown", options=_OPTIONS(), value="placa", clearable=False),
                dcc.Input(className="input veiculos--pesquisa", id="veiculos--input", type="search", debounce=False,
                    placeholder="Pesquisar motorista por CPF...")
                ]),
            html.Div(id="veiculos--lista", style={"padding-right": "5px"}, children=_LISTA(_BUSCA()))
            ]),
        html.Div(className="card veiculos--informacoes", id="veiculos--informacoes")
        ])


def _OPTIONS():
    return [
        {"label": "Placa", "value": "placa"},
        {"label": "Marca", "value": "marca"}
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


# @dash.callback(
#     Output("veiculos--input", "placeholder"),
#     Input("veiculos--dropdown", "value"),
#     prevent_initial_call=True
#     )
# def atualizar_placeholder(filtro: str):
#     return f"Pesquisar veículo por {filtro}..."

# @dash.callback(
#     Output("veiculos--lista", "children"),
#     Output("veiculos--lista", "style"),
#     Input("veiculos--input", "value"),
#     State("veiculos--dropdown", "value"),
#     prevent_initial_call=True
#     )
# def filtrar_veiculos(busca: str, filtro: str):
#     veiculos = _BUSCA(busca, filtro)

#     def lista_children():
#         return _LISTA(veiculos)
    
#     def lista_style():
#         return {"padding-right": "5px"} if len(veiculos) > 4 else {"padding-right": "0"}

#     return lista_children(), lista_style()


# @dash.callback(
#     Output("veiculos--informacoes", "children"),
#     Input("motoristas--url", "search")
#     )
# def informacoes_veiculo(url: str):
#     query = dict()
#     veiculo = None
#     em_viagem = None
#     id_entrega = None

#     banco_dados = database.BancoDados()
#     img_nomes = [img.split(".")[0] for img in listdir("./assets/images/veiculos/")]
#     img_arquivos = listdir("./assets/images/veiculos/")

#     def _QUERY():
#         nonlocal query
#         for arg in url.split("?")[1:]:
#             var, valor = arg.split("=")
#             query[var] = valor

#     def _VEICULO():
#         nonlocal veiculo
#         if url == "":
#             veiculo = _BUSCA()[0]
#         else:
#             veiculo = banco_dados.veiculos_busca(query["placa"])

#     def _STATUS():
#         nonlocal em_viagem, id_entrega
#         entregas_andamento = banco_dados.entregas_andamento()
#         for entrega in entregas_andamento:
#             if veiculo[1] == entrega[1]:
#                 em_viagem = True
#                 id_entrega = entrega[0]
#         else:
#             em_viagem = False

#     _QUERY()
#     _VEICULO()
#     _STATUS()

#     banco_dados.finalizar()

#     return [
#         html.Img(src=dash.get_asset_url(f"images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
#             width="260px", height="325px")
#         if veiculo[1] in img_nomes else
#         html.Div(className="sem-imagem veiculos--informacoes", children=html.Img(
#             src=dash.get_asset_url("icons/icone-camera.svg"), width="100px", height="100px"
#             )),
#         html.Div(className="conteudo", children=[
#             html.Div(className="informacoes-basicas", children=[
#                 html.P(f"Placa: {veiculo[1]}"),
#                 html.P(f"Marca: {veiculo[2]}"),
#                 html.P(f"Cor do Veículo: {veiculo[3]}"),
#                 html.P(f"Ano do Veículo: {veiculo[4]}"),
#                 html.P(f"Vencimento dos Documentos: {veiculo[5]}")
#                 ]),
#             html.Div(className="status", children=[
#                 dcc.Link(href=f"/entregas?id={id_entrega}", children="Veículo em viagem...")
#                 if em_viagem else
#                 html.P(children="Veículo em espera...")
#                 ])
#             ])
#         ]
