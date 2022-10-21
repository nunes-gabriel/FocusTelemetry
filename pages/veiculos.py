from dash import html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from PIL import Image
from string import punctuation
from os import listdir, remove
from io import BytesIO

import os
import re
import base64
import datetime
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
        dcc.Location(id="pg2--url", refresh=False),
        html.Div(className="card search-B s-B1", children=[
            html.H1("Veículos"),
            html.P("Escolha um veículo para acessar suas informações e/ou edite ou cadastre um novo veículo no sistema."),
            html.Div(className="row search-B", children=[
                dcc.Dropdown(className="dropdown search-B", id="pg2--search-filter",
                             options=Utils.options(), value="placa", clearable=False),
                dcc.Input(className="input search-B", id="pg2--search-bar", type="search", debounce=False,
                          placeholder="Pesquisar veículo por placa..."),
                html.Button(className="button-search-B click", n_clicks=0, id="pg2--mod0-abrir", children=html.Img(
                    src=dash.get_asset_url("icons/icone-adicionar.svg"), width="32px", height="32px"
                    ))
                ]),
            html.Div(className="card-list", id="pg2--lista", style={"padding-right": "5px"}, children=Layouts.cardlist(Utils.busca()))
            ]),
        html.Div(className="card infos-B i-B1", id="pg2--informacoes"),
        html.Div(className="layout-stats-A st-A1", children=Layouts.stats()),
        html.Div(className="modal-div", children=[
            Layouts.forms(n=0),
            Layouts.forms(n=1),
            Layouts.erro_upload()
            ])
        ])


class Layouts:
    @staticmethod
    def forms(n=0):
        """Modal para cadastro e edição de veículos no banco de dados."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id=f"pg2--mod{n}", children=[
            dcc.Location(id=f"pg2--mod{n}-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id=f"pg2--mod{n}-backdrop"),
            html.Div(className="card modal-body", id=f"pg2--mod{n}-conteudo", children=[
                html.H1("Registrar Veículo" if n == 0 else "Editar Veículo"),
                html.Form(className="modal-form", children=[
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Placa"),
                            dcc.Input(className="input", disabled=False if n == 0 else True, type="text", minLength=7, maxLength=7, id=f"pg2--mod{n}-forms1")])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Marca"),
                            dcc.Input(className="input", type="text", id=f"pg2--mod{n}-forms2")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Tipo de Veículo"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, options=[{"label": "Tração", "value": "Tração"}],
                                        value="Tração", id=f"pg2--mod{n}-forms3"),
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Tipo de Carroceria"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, id=f"pg2--mod{n}-forms7", value="Aberta", options=[
                                {"label": "Aberta", "value": "Aberta"},
                                {"label": "Báu Fechado ", "value": "Báu Fechado"},
                                {"label": "Báu Frigorificado", "value": "Báu Frigorificado"},
                                {"label": "Cegonha ", "value": "Cegonha"},
                                {"label": "Granaleira", "value": "Granaleira"},
                                {"label": "Porta-Container", "value": "Porta-Container"},
                                {"label": "Sider", "value": "Sider"},
                                {"label": "Tanque ", "value": "Tanque "}
                                ])
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Código Renavam"),
                            dcc.Input(className="input", type="text", pattern=u"[0-9]+", maxLength=11, id=f"pg2--mod{n}-forms5")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Ano do Veículo"),
                            dcc.Input(className="input", type="number", min=1980, max=datetime.datetime.today().year, id=f"pg2--mod{n}-forms6")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-datepicker", children="Documentação"),
                            dcc.DatePickerSingle(className="form-field datepicker", placeholder="Data", display_format="DD/MM/YYYY",
                                                id=f"pg2--mod{n}-forms13")])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Cor"),
                            dcc.Input(className="input", type="text", id=f"pg2--mod{n}-forms4")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Altura(m)"),
                            dcc.Input(className="input", type="number", id=f"pg2--mod{n}-forms8")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Largura(m)"),
                            dcc.Input(className="input", type="number", id=f"pg2--mod{n}-forms9")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Comprimento(m)"),
                            dcc.Input(className="input", type="number", id=f"pg2--mod{n}-forms10")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Tara(kg)"),
                            dcc.Input(className="input", type="number", id=f"pg2--mod{n}-forms11")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Capacidade(kg)"),
                            dcc.Input(className="input", type="number", id=f"pg2--mod{n}-forms12")
                            ])
                        ])
                    ]),  
                html.Div(style={"color": "red", "font-size": "11px"}, id=f"pg2--mod{n}-forms-feedback"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id=f"pg2--mod{n}-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id=f"pg2--mod{n}-cancelar", children="Cancelar")
                    ])
                ])
            ])

    @staticmethod
    def deletar(placa: str):
        """Modal para confirmação de deletar veículo."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg2--mod2", children=[
            dcc.Location(id="pg2--mod2-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id="pg2--mod2-backdrop"),
            html.Div(className="card modal-body", id="pg2--mod2-conteudo", children=[
                html.H3(style={"margin-top": "15px"}, children="Tem certeza que deseja deletar o veículo do banco de dados?"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", value=placa, n_clicks=0, id="pg2--mod2-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id="pg2--mod2-cancelar", children="Cancelar"),
                    ])
                ])
            ])

    @staticmethod
    def erro_upload():
        """Modal para erro de upload de imagens."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg2--mod3", children=[
            html.Button(className="modal-backdrop", n_clicks=0, id="pg2--mod3-backdrop"),
            html.Div(className="card modal-body", id="pg2--mod3-conteudo", children=[
                html.H3(style={"margin-top": "15px", "margin-bottom": "15px"}, children="Erro ao fazer upload de imagem, tamanho ou formato inválido.")
                ])
            ])

    @staticmethod
    def cardlist(veiculos: tuple):
        """Lista de cards com os veículos registrados no banco de dados."""
        img_arquivos = listdir(Utils.assets_path() + "\\assets\\images\\veiculos\\")
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
    
    @staticmethod
    def stats():
        """Status da frota de veículos da transportadora."""
        banco_dados = database.BancoDados()
        veiculos = banco_dados.veiculos_lista()

        return [
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-viagem.svg"), width="120px", height="120px"),
                html.H2("Em viagem"),
                html.H1(len([v for v in veiculos if v[-1] == "Em Viagem "]))
                ]),
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-veiculo-disponivel.svg"), width="120px", height="120px"),
                html.H2("Disponíveis"),
                html.H1(len([v for v in veiculos if v[-1] == "Disponível"]))
                ]),
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-chave.svg"), width="120px", height="120px"),
                html.H2("Manutenção"),
                html.H1(len([v for v in veiculos if v[-1] == "Em Manutenção "]))
                ])
            ]


class Utils:
    @staticmethod
    def options():
        """Opções de filtros para a barra de pesquisa."""
        return [
            {"label": "Placa", "value": "placa"},
            {"label": "Marca", "value": "marca"}
            ]

    @staticmethod
    def assets_path():
        return os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)

    @staticmethod
    def busca(busca=None, filtro=None):
        """Busca um veículo no banco de dados através de uma pesquisa."""
        banco_dados = database.BancoDados()
        veiculos = banco_dados.veiculos_lista()
        if busca not in [None, ""]:
            for index, opcao in enumerate(Utils.options()):
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
    
    @staticmethod
    def query(query: str):
        """Filtra a query do endereço URL da página."""
        filtered_query = dict()
        for arg in query.split("?")[1:]:
            var, value = arg.split("=")
            filtered_query[var] = value
        return filtered_query

    @staticmethod
    def veiculo(query: str):
        """Busca por um veículo no banco de dados de acordo com a sua placa."""
        if "placa" not in query:
            veiculo = Utils.busca()[0]
        else:
            banco_dados = database.BancoDados()
            veiculo = banco_dados.veiculos_busca(Utils.query(query)["placa"])
            banco_dados.finalizar()
        return veiculo

    @staticmethod
    def filtrar(forms: tuple):
        """Filtra os formulários de cadastro e edição para evitar erros no banco de dados."""
        if any(form in [None, "", 0] for form in forms):
            return "Um dos campos do formulários está vazio ou com um valor inválido."
        elif len(forms[0]) < 7 or any(c in punctuation for c in forms[0]):
            return "A placa de veículo inserida é inválida."
        elif any(any([str.isdigit(c), c in punctuation]) for c in forms[3]):
            return "A cor do veículo inserida é inválida."
        elif len(forms[4]) < 11 or any(not str.isdigit(c) for c in forms[4]):
            return "O código de RENAVAM inserido é inválido."
        elif 1980 < int(forms[5]) > datetime.datetime.today().year:
            return "O ano do veículo inserido é inválido."
        else:
            try:
                dia, mes, ano = [int(d) for d in forms[-1].split("/")]
                datetime.date(ano, mes, dia)
            except:
                return "A data de validade dos documentos inserida é inválida."
            finally:
                return None


@dash.callback(
    Output("pg2--search-bar", "placeholder"),
    Input("pg2--search-filter", "value"),
    prevent_initial_call=True
    )
def placeholder(filtro: str):
    """Atualiza o placeholder da barra de pesquisas de acordo com o filtro atual."""
    return f"Pesquisar veículo por {filtro}..."


@dash.callback(
    Output("pg2--lista", "children"),
    Output("pg2--lista", "style"),
    Input("pg2--search-bar", "value"),
    State("pg2--search-filter", "value"),
    prevent_initial_call=True
    )
def barra_busca(busca: str, filtro: str):
    """Realiza uma busca no banco de dados através da barra de pesquisa."""
    veiculos = Utils.busca(busca, filtro)
    return Layouts.cardlist(veiculos), {"padding-right": "5px"} if len(veiculos) > 4 else {"padding-right": "0"}


@dash.callback(
    Output("pg2--informacoes", "children"),
    Input("pg2--url", "search")
    )
def atualizar_informacoes(url: str):
    """Atualiza o card de informações de acordo com o veículo selecionado da lista."""
    id_entrega = None
    veiculo = Utils.veiculo(url)

    img_arquivos = listdir(Utils.assets_path() + "\\assets\\images\\veiculos\\")
    img_nomes = [img.split(".")[0] for img in img_arquivos]

    return [
        html.Img(className="image", src=dash.get_asset_url(f"images/veiculos/{img_arquivos[img_nomes.index(veiculo[1])]}"),
                width="260px", height="325px")
        if veiculo[1] in img_nomes else
        html.Div(className="no-img infos-B", children=html.Img(
            src=dash.get_asset_url("icons/icone-camera.svg"), width="100px", height="100px"
            )),
        html.Div(className="content", children=[
            html.Div(className="infos-list", children=[
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
            html.Button(className="button-infos-B click", n_clicks=0, id="pg2--mod2-abrir", children=html.Img(
                src=dash.get_asset_url("icons/icone-lixeira.svg"), width="35px", height="35px"
                )),
            dcc.Location(id="pg2--upload-refresh", refresh=False),
            dcc.Upload(id="pg2--upload", children=[
                html.Button(className="button-infos-B click", n_clicks=0, children=[
                    html.Img(src=dash.get_asset_url("icons/icone-imagem.svg"), width="35px", height="35px")
                    ])
                ]),
            html.Button(className="button-infos-B click", n_clicks=0, id=f"pg2--mod1-abrir", children=html.Img(
                src=dash.get_asset_url("icons/icone-editar.svg"), width="35px", height="35px"
                )),
            ]),
        Layouts.deletar(veiculo[1])
        ]


@dash.callback(
    Output("pg2--mod0", "style"),
    Input("pg2--mod0-abrir", "n_clicks"),
    Input("pg2--mod0-backdrop", "n_clicks"),
    Input("pg2--mod0-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def forms_novo_abrir(*bt):
    """Abre o modal de formulário para cadastro de veículos no banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg2--mod0-backdrop", "pg2--mod0-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg2--mod0-refresh", "refresh"),
    Output("pg2--mod0-refresh", "pathname"),
    Output("pg2--mod0-forms-feedback", "children"),
    Input("pg2--mod0-confirmar", "n_clicks"),
    State("pg2--mod0-refresh", "pathname"),
    [State(f"pg2--mod0-forms{i}", "value") for i in range(1, 13)],
    State("pg2--mod0-forms13", "date"),
    prevent_initial_call=True
    )
def forms_novo_confirmar(bt, path, *forms):
    """Registra um veículo no banco de dados com os dados inseridos no formulário."""
    if bt:
        banco_dados = database.BancoDados()

        erro = Utils.filtrar(forms)
        if erro is not None:
            return *[dash.no_update] * 2, erro

        forms = list(forms)
        forms[0] = forms[0][:3] + "-" + forms[0][3:]

        placas = banco_dados.veiculos_placas()
        for placa in placas:
            if forms[0] == placa[0]:
                return *[dash.no_update] * 2, "A placa inserida já existe no banco de dados."

        banco_dados.veiculos_criar(forms)

        if path == "/veiculos/":
            return True, "/veiculos", dash.no_update
        else:
            return True, "/veiculos/", dash.no_update
    else:
        raise PreventUpdate


@dash.callback(
    Output(f"pg2--mod1-forms13", "date"),
    [Output(f"pg2--mod1-forms{i}", "value") for i in range(1, 13)],
    Input("pg2--url", "search")
    )
def forms_editar_atualizar(url):
    """Preenche o modal de edição do veículo com as informações já cadastradas do banco de dados."""
    veiculo = Utils.veiculo(url)
    return [veiculo[-2]] + list(veiculo[1:-2])


@dash.callback(
    Output("pg2--mod1", "style"),
    Input("pg2--mod1-abrir", "n_clicks"),
    Input("pg2--mod1-backdrop", "n_clicks"),
    Input("pg2--mod1-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def forms_editar_abrir(*bt):
    """Abre o modal de formulário para edição de veículos do banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg2--mod1-backdrop", "pg2--mod1-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg2--mod1-refresh", "refresh"),
    Output("pg2--mod1-refresh", "pathname"),
    Output("pg2--mod1-forms-feedback", "children"),
    Input("pg2--mod1-confirmar", "n_clicks"),
    State("pg2--mod1-refresh", "pathname"),
    [State(f"pg2--mod1-forms{i}", "value") for i in range(1, 13)],
    State(f"pg2--mod1-forms13", "date"),
    prevent_initial_call=True
    )
def forms_editar_confirmar(bt, path, *forms):
    """Confirma a edição das informações do veículo no banco de dados."""
    if bt:
        banco_dados = database.BancoDados()

        erro = Utils.filtrar(forms)
        if erro is not None:
            return *[dash.no_update] * 2, erro

        banco_dados.veiculos_atualizar(forms[0], forms[1:])

        if path == "/veiculos/":
            return True, "/veiculos", dash.no_update
        else:
            return True, "/veiculos/", dash.no_update
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg2--mod2", "style"),
    Input("pg2--mod2-abrir", "n_clicks"),
    Input("pg2--mod2-backdrop", "n_clicks"),
    Input("pg2--mod2-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def deletar_abrir(*bt):
    """Abre o modal de confirmação para deletar o veículo selecionado do banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg2--mod2-backdrop", "pg2--mod2-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg2--mod2-refresh", "refresh"),
    Output("pg2--mod2-refresh", "pathname"),
    Output("pg2--mod2-refresh", "search"),
    Input("pg2--mod2-confirmar", "n_clicks"),
    State("pg2--mod2-confirmar", "value"),
    State("pg2--mod2-refresh", "pathname"),
    prevent_initial_call=True
    )
def deletar_confirmar(bt, placa, path):
    """Confirma a exclusão do veículo selecionado do banco de dados."""
    if bt:
        banco_dados = database.BancoDados()
        banco_dados.veiculos_deletar(placa)
        banco_dados.finalizar()

        img_arquivos = listdir(Utils.assets_path() + "\\assets\\images\\veiculos\\")
        img_nomes = [img.split(".")[0] for img in img_arquivos]
        if placa in img_nomes:
            remove(f"./assets/images/veiculos/{img_arquivos[img_nomes.index(placa)]}")

        if path == "/veiculos/":
            return True, "/veiculos", ""
        else:
            return True, "/veiculos/", ""
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg2--upload-refresh", "refresh"),
    Output("pg2--upload-refresh", "pathname"),
    Output("pg2--mod3", "style"),
    Input("pg2--mod3-backdrop", "n_clicks"),
    Input("pg2--upload", "contents"),
    State("pg2--upload", "filename"),
    State("pg2--url", "search"),
    State("pg2--upload-refresh", "pathname"),
    prevent_initial_call=True
    )
def upload_imagem(bt, img, filename, query, path):
    """Upload de imagem de veículo para o dashboard com mensagem de erro."""
    if img is not None and ctx.triggered_id == "pg2--upload":
        try:
            img = re.sub("^data:image/.+;base64,", "", img)
            img_b64 = base64.b64decode(img)
            imagem = Image.open(BytesIO(img_b64))
            imagem = imagem.resize((260, 325))
            imagem.save(f"./assets/images/veiculos/{Utils.veiculo(query)[1]}.{filename.split('.')[1]}")
            if path == "/veiculos/":
                return True, "/veiculos", dash.no_update
            else:
                return True, "/veiculos/", dash.no_update
        except:
            return *[dash.no_update] * 2, {"visibility": "visible"}
    elif ctx.triggered_id == "pg2--mod3-backdrop":
        return *[dash.no_update] * 2, {"visibility": "hidden"}
    else:
        raise PreventUpdate
