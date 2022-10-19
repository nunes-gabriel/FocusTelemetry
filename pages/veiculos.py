from dash import html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from os import listdir, remove

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
        html.Div(className="card search-B", children=[
            html.H1("Veículos"),
            html.P("Escolha um veículo para análise e/ou edição ou cadastre um novo veículo no sistema."),
            html.Div(className="row search-B", children=[
                dcc.Dropdown(className="dropdown search-B", id="veiculos--dropdown",
                             options=dropdown_options(), value="placa", clearable=False),
                dcc.Input(className="input search-B", id="veiculos--input", type="search", debounce=False,
                          placeholder="Pesquisar veículo por placa..."),
                html.Button(className="button-search-B click", n_clicks=0, id="veiculos--modal-abrir-novo", children=html.Img(
                    src=dash.get_asset_url("icons/icone-adicionar.svg"), width="32px", height="32px"
                    ))
                ]),
            html.Div(id="veiculos--lista", style={"padding-right": "5px"}, children=listar_veiculos(filtro_busca()))
            ]),
        html.Div(className="card infos-B", id="veiculos--informacoes"),
        html.Div(className="modal", style={"visibility": "hidden"}, id="veiculos--modal", children=[
            html.Button(className="modal-backdrop", n_clicks=0, id="veiculos--modal-fechar-backdrop"),
            html.Div(className="card modal-body", id="veiculos--modal-conteudo", children=[
                html.H1("Registrar Veículo"),
                html.Form(className="modal-form", children=[
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Placa"),
                            dcc.Input(className="input", type="text", maxLength=7, id="veiculos--forms-0")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Marca"),
                            dcc.Input(className="input", type="text", id="veiculos--forms-1")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Tipo de Veículo"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, options=[{"label": "Tração", "value": "Tração"}],
                                         value="Tração", id="veiculos--forms-2"),
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-datepicker", children="Documentação"),
                            dcc.DatePickerSingle(className="form-field datepicker", placeholder="Data", display_format="DD/MM/YYYY",
                                                 id="veiculos--forms-3")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Cor"),
                            dcc.Input(className="input", type="text", id="veiculos--forms-4")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Código Renavam"),
                            dcc.Input(className="input", type="text", pattern=u"[0-9]+", maxLength=11, id="veiculos--forms-5")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Ano do Veículo"),
                            dcc.Input(className="input", type="number", min=1980, id="veiculos--forms-6")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Tipo de Carroceria"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, id="veiculos--forms-7", value="Aberta", options=[
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
                            dcc.Input(className="input", type="number", id="veiculos--forms-8")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Largura(m)"),
                            dcc.Input(className="input", type="number", id="veiculos--forms-9")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Comprimento(m)"),
                            dcc.Input(className="input", type="number", id="veiculos--forms-10")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Tara(kg)"),
                            dcc.Input(className="input", type="number", id="veiculos--forms-11")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Capacidade(kg)"),
                            dcc.Input(className="input", type="number", id="veiculos--forms-12")
                            ])
                        ])
                    ]),
                html.Div(id="veiculos--forms-feedback"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id="veiculos--modal-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id="veiculos--modal-fechar-cancelar", children="Cancelar")
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
    id_entrega = None

    veiculo = veiculo_informacoes(url)

    img_arquivos = listdir("./assets/images/veiculos/")
    img_nomes = [img.split(".")[0] for img in img_arquivos]

    return [
        html.Img(className="imagem-informacoes", src=dash.get_asset_url(f"images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
                 width="260px", height="325px")
        if veiculo[1] in img_nomes else
        html.Div(className="no-img infos-B", children=html.Img(
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
        html.Div(className="buttons-layout", children=[
            dcc.ConfirmDialogProvider(id="veiculos--deletar", message="Tem certeza que deseja deletar o veículo selecionado?", children=html.Button(
                n_clicks=0, className="button-infos-B click", children=html.Img(
                    src=dash.get_asset_url("icons/icone-lixeira.svg"), width="30px", height="30px"
                    )
                )),
            html.Button(className="button-infos-B click", n_clicks=0, id="veiculos--modal-abrir-edicao", children=html.Img(
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
        raise PreventUpdate
    else:
        banco_dados = database.BancoDados()
        placa_veiculo = veiculo_informacoes(query=query)[1]

        banco_dados.veiculos_deletar(placa_veiculo)
        banco_dados.finalizar()

        img_arquivos = listdir("./assets/images/veiculos/")
        img_nomes = [img.split(".")[0] for img in img_arquivos]

        if placa_veiculo in img_nomes:
            remove(f"./assets/images/veiculos/{img_arquivos[img_nomes.index(placa_veiculo)]}")

        if path == "/veiculos/":
            return True, "/veiculos", ""
        else:
            return True, "/veiculos/", ""


@dash.callback(
    Output("veiculos--modal", "style"),
    Input("veiculos--modal-abrir-novo", "n_clicks"),
    Input("veiculos--modal-abrir-edicao", "n_clicks"),
    Input("veiculos--modal-fechar-backdrop", "n_clicks"),
    Input("veiculos--modal-fechar-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def abrir_modal(b1, b2, b3, b4):
    if b1 or b2 or b3 or b4:
        if ctx.triggered_id in ["veiculos--modal-fechar-backdrop", "veiculos--modal-fechar-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        raise PreventUpdate


@dash.callback(
    Output("veiculos--forms-feedback", "children"),
    Output("veiculos--forms-feedback", "style"),
    Input("veiculos--modal-confirmar", "n_clicks"),
    [State(f"veiculos--forms-{i}", "value") if i != 3 else State(f"veiculos--forms-{i}", "date") for i in range(12)],
    prevent_initial_call=True
    )
def registrar_veiculo(bt, *forms):
    raise PreventUpdate
