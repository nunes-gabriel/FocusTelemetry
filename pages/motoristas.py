from dash import html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from PIL import Image
from string import punctuation
from os import listdir, remove
from io import BytesIO

import os
import re
import base64
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
        dcc.Location(id="pg3--url", refresh=False),
        html.Div(className="card search-B s-B2", children=[
            html.H1("Motoristas"),
            html.P("Escolha um motorista para acessar suas informações e/ou edite ou cadastre um novo motorista no sistema."),
            html.Div(className="row search-B", children=[
                dcc.Dropdown(className="dropdown search-B", id="pg3--search-filter",
                             options=Utils.options(), value="nome", clearable=False),
                dcc.Input(className="input search-B", id="pg3--search-bar", type="search", debounce=False,
                          placeholder="Pesquisar motorista por nome..."),
                html.Button(className="button-search click", n_clicks=0, id="pg3--mod0-abrir", children=html.Img(
                    src=dash.get_asset_url("icons/icone-adicionar.svg"), width="32px", height="32px"
                    ))
                ]),
            html.Div(className="card-list", id="pg3--lista", style={"padding-right": "5px"}, children=Layouts.cardlist(Utils.busca()))
            ]),
        html.Div(className="card infos-B i-B2", id="pg3--informacoes"),
        html.Div(className="layout-stats-A st-A2", children=Layouts.stats()),
        html.Div(className="modal-div", children=[
            Layouts.forms(n=0),
            Layouts.forms(n=1),
            Layouts.erro_upload()
            ])
        ])


class Layouts:
    @staticmethod
    def forms(n=0):
        """Modal para cadastro e edição de motoristas no banco de dados."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id=f"pg3--mod{n}", children=[
            dcc.Location(id=f"pg3--mod{n}-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id=f"pg3--mod{n}-backdrop"),
            html.Div(className="card modal-body", id=f"pg3--mod{n}-conteudo", children=[
                html.H1("Registrar Motorista" if n == 0 else "Editar Motorista"),
                html.Form(className="modal-form", children=[
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("CPF"),
                            dcc.Input(className="input", disabled=False if n == 0 else True, type="text", pattern=u"[0-9]+", minLength=11, maxLength=11, id=f"pg3--mod{n}-forms4")])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("RG"),
                            dcc.Input(className="input", disabled=False if n == 0 else True, type="text", pattern=u"[0-9]+", minLength=9, maxLength=9, id=f"pg3--mod{n}-forms3")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Nome Completo"),
                            dcc.Input(className="input", type="text", id=f"pg3--mod{n}-forms1")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Idade"),
                            dcc.Input(className="input", type="number", min=18, max=120, step=1, id=f"pg3--mod{n}-forms2")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Telefone #1"),
                            dcc.Input(className="input", type="tel", pattern=u"[0-9]+", minLength=10, maxLength=11, id=f"pg3--mod{n}-forms5")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Telefone #2"),
                            dcc.Input(className="input", type="tel", pattern=u"[0-9]+", minLength=10, maxLength=11, id=f"pg3--mod{n}-forms6")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Endereço de CEP"),
                            dcc.Input(className="input", type="text", pattern=u"[0-9]+", minLength=8, maxLength=8, id=f"pg3--mod{n}-forms7")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Rua"),
                            dcc.Input(className="input", type="text", id=f"pg3--mod{n}-forms8")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Bairro"),
                            dcc.Input(className="input", type="text", id=f"pg3--mod{n}-forms9")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Número"),
                            dcc.Input(className="input", type="number", step=1, id=f"pg3--mod{n}-forms10")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Cidade"),
                            dcc.Input(className="input", type="text", id=f"pg3--mod{n}-forms11")
                            ])
                        ]), 
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Estado"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, options=Utils.estados(),
                                        value="SC", id=f"pg3--mod{n}-forms12"),
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Habilitação"),
                            dcc.Input(className="input", type="text", pattern=u"[0-9]+", minLength=11, maxLength=11, id=f"pg3--mod{n}-forms13")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Categoria de Hab."),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, id=f"pg3--mod{n}-forms14", multi=True, value="Aberta", options=[
                                {"label": "A", "value": "A"},
                                {"label": "B", "value": "B"},
                                {"label": "C", "value": "C"},
                                {"label": "D", "value": "D"},
                                {"label": "E", "value": "E"}
                                ])
                            ])
                        ])
                    ]),  
                html.Div(style={"color": "red", "font-size": "11px"}, id=f"pg3--mod{n}-forms-feedback"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id=f"pg3--mod{n}-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id=f"pg3--mod{n}-cancelar", children="Cancelar")
                    ])
                ])
            ])

    @staticmethod
    def deletar(cpf: str):
        """Modal para confirmação de deletar motorista."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg3--mod2", children=[
            dcc.Location(id="pg3--mod2-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id="pg3--mod2-backdrop"),
            html.Div(className="card modal-body", id="pg3--mod2-conteudo", children=[
                html.H3(style={"margin-top": "15px"}, children="Tem certeza que deseja deletar o motorista do banco de dados?"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", value=cpf, n_clicks=0, id="pg3--mod2-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id="pg3--mod2-cancelar", children="Cancelar"),
                    ])
                ])
            ])

    @staticmethod
    def erro_upload():
        """Modal para erro de upload de imagens."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg3--mod3", children=[
            html.Button(className="modal-backdrop", n_clicks=0, id="pg3--mod3-backdrop"),
            html.Div(className="card modal-body", id="pg3--mod3-conteudo", children=[
                html.H3(style={"margin-top": "15px", "margin-bottom": "15px"}, children="Erro ao fazer upload de imagem, tamanho ou formato inválido.")
                ])
            ])

    @staticmethod
    def cardlist(motoristas: tuple):
        """Lista de cards com os motoristas registrados no banco de dados."""
        img_arquivos = listdir(Utils.assets_path() + "\\assets\\images\\motoristas\\")
        img_nomes = [img.split(".")[0] for img in img_arquivos]

        return [
            dcc.Link(style={"text-decoration": "none"}, href=f"/motoristas?cpf={motorista[4]}", refresh=False, children=[
                html.Div(className="card-list-item click", children=[
                    html.Img(src=dash.get_asset_url(f"images/motoristas/{img_arquivos[img_nomes.index(motorista[4])]}"),
                            width="100px", height="100px")
                    if motorista[1] in img_nomes else
                    html.Div(className="no-img", children=html.Img(
                        src=dash.get_asset_url("icons/icone-camera.svg"), width="45px", height="45px"
                        )),
                    html.Div(children=[
                        html.P(style={"line-height": "16px"}, children=f"Nome: {motorista[1]}"),
                        html.P(f"CPF: {motorista[4]}")
                        ])
                    ])
                ])
            for motorista in motoristas
            ]
    
    @staticmethod
    def stats():
        """Status dos motoristas da transportadora."""
        banco_dados = database.BancoDados()
        motoristas = banco_dados.motoristas_lista()
        banco_dados.finalizar()

        return [
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-volante.svg"), width="70px", height="70px"),
                html.H2("Em viagem"),
                html.H1(len([v for v in motoristas if v[-1] in ["Em Viagem ", "Em Viagem"]]))
                ]),
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-motorista-disponivel.svg"), width="70px", height="70px"),
                html.H2("Disponíveis"),
                html.H1(len([v for v in motoristas if v[-1] in ["Disponível ", "Disponível"]]))
                ]),
            html.Div(className="card stats-A", children=[
                html.Img(src=dash.get_asset_url("icons/icone-afastado.svg"), width="70px", height="70px"),
                html.H2("Afastados"),
                html.H1(len([v for v in motoristas if v[-1] in ["Afastado", "Afastado "]]))
                ])
            ]


class Utils:
    @staticmethod
    def options():
        """Opções de filtros para a barra de pesquisa."""
        return [
            {"label": "Nome", "value": "nome"},
            {"label": "CPF", "value": "CPF"},
            ]

    @staticmethod
    def assets_path():
        return os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)

    @staticmethod
    def estados():
        """Lista de estados e siglas para criação de dropdown."""
        return [
            {'label': 'Acre', 'value': 'AC'},
            {'label': 'Alagoas', 'value': 'AL'},
            {'label': 'Amapá', 'value': 'AP'},
            {'label': 'Amazonas', 'value': 'AM'},
            {'label': 'Bahia', 'value': 'BA'},
            {'label': 'Ceará', 'value': 'CE'},
            {'label': 'Distrito Federal', 'value': 'DF'},
            {'label': 'Espírito Santo', 'value': 'ES'},
            {'label': 'Goiás', 'value': 'GO'},
            {'label': 'Maranhão', 'value': 'MA'},
            {'label': 'Mato Grosso', 'value': 'MT'},
            {'label': 'Mato Grosso do Sul', 'value': 'MS'},
            {'label': 'Minas Gerais', 'value': 'MG'},
            {'label': 'Pará', 'value': 'PA'},
            {'label': 'Paraíba', 'value': 'PB'},
            {'label': 'Paraná', 'value': 'PR'},
            {'label': 'Pernambuco', 'value': 'PE'},
            {'label': 'Piauí', 'value': 'PI'},
            {'label': 'Rio de Janeiro', 'value': 'RJ'},
            {'label': 'Rio Grande do Norte', 'value': 'RN'},
            {'label': 'Rio Grande do Sul', 'value': 'RS'},
            {'label': 'Rondônia', 'value': 'RO'},
            {'label': 'Roraima', 'value': 'RR'},
            {'label': 'Santa Catarina', 'value': 'SC'},
            {'label': 'São Paulo', 'value': 'SP'},
            {'label': 'Sergipe', 'value': 'SE'},
            {'label': 'Tocantins', 'value': 'TO'}
            ]

    @staticmethod
    def busca(busca=None, filtro=None):
        """Busca um motorista no banco de dados através de uma pesquisa."""
        banco_dados = database.BancoDados()
        motoristas = banco_dados.motoristas_lista()
        if busca not in [None, ""]:
            opcoes = {1: "nome", 4: "CPF"}
            for index, opcao in opcoes.items():
                if opcao == filtro:
                    break
            busca = busca.upper()
            motoristas_filtrado = list()
            for motorista in motoristas:
                if motorista[index].upper().startswith(busca):
                    motoristas_filtrado.append(motorista)
            motoristas = motoristas_filtrado
        banco_dados.finalizar()
        return motoristas
    
    @staticmethod
    def query(query: str):
        """Filtra a query do endereço URL da página."""
        filtered_query = dict()
        for arg in query.split("?")[1:]:
            var, value = arg.split("=")
            filtered_query[var] = value
        return filtered_query

    @staticmethod
    def motorista(query: str):
        """Busca por um motorista no banco de dados de acordo com seu CPF."""
        if query is None or "cpf" not in query:
            motorista = Utils.busca()[0]
        else:
            banco_dados = database.BancoDados()
            motorista = banco_dados.motoristas_busca(Utils.query(query)["cpf"])
            banco_dados.finalizar()
        return motorista

    @staticmethod
    def filtrar(forms: tuple):
        """Filtra os formulários de cadastro e edição para evitar erros no banco de dados."""
        if any(form in [None, "", 0] for form in forms[:5] + forms[6:]):
            return "Um dos campos do formulários está vazio ou com um valor inválido."    
        elif any(any([str.isdigit(c), c in punctuation]) for c in forms[0]):
            return "O nome do motorista inserido é inválido."
        elif 18 < forms[1] > 120 or not isinstance(forms[1], int):
            return "A idade do motorista inserida é inválida."
        elif len(forms[2]) < 9 or any(not str.isdigit(c) for c in forms[2]):
            return "O RG do motorista inserido é inválido."
        elif len(forms[3]) < 11 or any(not str.isdigit(c) for c in forms[3]):
            return "O CPF do motorista inserido é inválido."
        elif len(forms[4]) < 10 or any(not str.isdigit(c) for c in forms[4]):
            return "O telefone do motorista inserido é inválido."
        elif forms[5] not in [None, ""] and (len(forms[5]) < 10 or any(not str.isdigit(c) for c in forms[5])):
            return "O telefone do motorista inserido é inválido."
        elif len(forms[6]) < 8 or any(not str.isdigit(c) for c in forms[6]):
            return "O CEP do motorista inserido é inválido."
        elif len(forms[-2]) < 11 or any(not str.isdigit(c) for c in forms[-2]):
            return "O registro de habilitação de motorista inserido é inválido."
        else:
            return None


@dash.callback(
    Output("pg3--search-bar", "placeholder"),
    Input("pg3--search-filter", "value"),
    prevent_initial_call=True
    )
def placeholder(filtro: str):
    """Atualiza o placeholder da barra de pesquisas de acordo com o filtro atual."""
    return f"Pesquisar motorista por {filtro}..."


@dash.callback(
    Output("pg3--lista", "children"),
    Output("pg3--lista", "style"),
    Input("pg3--search-bar", "value"),
    State("pg3--search-filter", "value"),
    prevent_initial_call=True
    )
def barra_busca(busca: str, filtro: str):
    """Realiza uma busca no banco de dados através da barra de pesquisa."""
    motoristas = Utils.busca(busca, filtro)
    return Layouts.cardlist(motoristas), {"padding-right": "5px"} if len(motoristas) > 4 else {"padding-right": "0"}


@dash.callback(
    Output("pg3--informacoes", "children"),
    Input("pg3--url", "search")
    )
def atualizar_informacoes(url: str):
    """Atualiza o card de informações de acordo com o motorista selecionado da lista."""
    motorista = Utils.motorista(url)

    banco_dados = database.BancoDados()
    id_entrega = banco_dados.entregas_motorista(motorista[4])
    banco_dados.finalizar()

    img_arquivos = listdir(Utils.assets_path() + "\\assets\\images\\motoristas\\")
    img_nomes = [img.split(".")[0] for img in img_arquivos]

    return [
        html.Img(className="image", src=dash.get_asset_url(f"images/motoristas/{img_arquivos[img_nomes.index(motorista[4])]}"),
                width="260px", height="325px")
        if motorista[4] in img_nomes else
        html.Div(className="no-img infos-B", children=html.Img(
            src=dash.get_asset_url("icons/icone-camera.svg"), width="100px", height="100px"
            )),
        html.Div(className="content", children=[
            html.Div(className="infos-list", children=[
                html.P(f"Nome Completo: {motorista[1]}"),
                html.P(f"CPF: {motorista[4]} | RG: {motorista[3]}"),
                html.P(f"Idade: {motorista[2]}"),
                html.P(f"Telefone(s): {motorista[5]}"),
                html.P(f"CEP: {motorista[6]}"),
                html.P(f"Endereço: {motorista[11]}, {motorista[10]}, {motorista[8]}, {motorista[7]}, {motorista[9]}"),
                html.P(f"Habilitação: {motorista[12]}"),
                html.Hr()
                ]),
            html.Div(className="status", children=[
                dcc.Link(href=f"/entregas?id={id_entrega[0]}", children="Motorista em viagem...")
                if motorista[-1] in ["Em Viagem ", "Em Viagem"] else
                html.P(children=f"Motorista {motorista[-1].lower()}")
                ])
            ]),
        html.Div(className="buttons-layout", children=[
            html.Button(className="button-infos-B last click", n_clicks=0, id="pg3--mod2-abrir", children=html.Img(
                src=dash.get_asset_url("icons/icone-lixeira.svg"), width="35px", height="35px"
                )),
            dcc.Location(id="pg3--upload-refresh", refresh=False),
            dcc.Upload(id="pg3--upload", children=[
                html.Button(className="button-infos-B click", n_clicks=0, children=[
                    html.Img(src=dash.get_asset_url("icons/icone-imagem.svg"), width="35px", height="35px")
                    ])
                ]),
            html.Button(className="button-infos-B click", n_clicks=0, id=f"pg3--mod1-abrir", children=html.Img(
                src=dash.get_asset_url("icons/icone-editar.svg"), width="35px", height="35px"
                )),
            ]),
        Layouts.deletar(motorista[4])
        ]


@dash.callback(
    Output("pg3--mod0", "style"),
    Input("pg3--mod0-abrir", "n_clicks"),
    Input("pg3--mod0-backdrop", "n_clicks"),
    Input("pg3--mod0-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def forms_novo_abrir(*bt):
    """Abre o modal de formulário para cadastro de motoristas no banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg3--mod0-backdrop", "pg3--mod0-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg3--mod0-refresh", "refresh"),
    Output("pg3--mod0-refresh", "pathname"),
    Output("pg3--mod0-forms-feedback", "children"),
    Input("pg3--mod0-confirmar", "n_clicks"),
    State("pg3--mod0-refresh", "pathname"),
    [State(f"pg3--mod0-forms{i}", "value") for i in range(1, 15)],
    prevent_initial_call=True
    )
def forms_novo_confirmar(bt, path, *forms):
    """Registra um motorista no banco de dados com os dados inseridos no formulário."""
    if bt:
        banco_dados = database.BancoDados()

        erro = Utils.filtrar(forms)
        if erro is not None:
            return *[dash.no_update] * 2, erro

        forms = list(forms)

        forms[3] = f"{forms[3][:3]}.{forms[3][3:6]}.{forms[3][6:9]}-{forms[3][9:]}"
        forms[2] = f"{forms[2][:2]}.{forms[2][2:5]}.{forms[2][5:8]}-{forms[2][-1]}"

        for rg_cpf in banco_dados.motoristas_identidade():
            if forms[3] == rg_cpf[1]:
                return *[dash.no_update] * 2, "O CPF inserido já existe no banco de dados."
            elif forms[2] == rg_cpf[0]:
                return *[dash.no_update] * 2, "O RG inserido já existe no banco de dados."

        forms[6] = f"{forms[6][:5]}-{forms[6][5:]}"
        forms[-1] = "/".join(forms[-1])

        tel2 = forms.pop(5)
        forms[4] = f"({forms[4][:2]}) {forms[4][2:-4]}-{forms[4][-4:]}"
        if tel2 not in ["", None]:
            forms[4] = f"{forms[4]} / ({tel2[:2]}) {tel2[2:-4]}-{tel2[-4:]}"

        banco_dados.motoristas_criar(forms)

        if path == "/motoristas/":
            return True, "/motoristas", dash.no_update
        else:
            return True, "/motoristas/", dash.no_update
    else:
        raise PreventUpdate


@dash.callback(
    [Output(f"pg3--mod1-forms{i}", "value") for i in range(1, 15)],
    Input("pg3--url", "search")
    )
def forms_editar_atualizar(url):
    """Preenche o modal de edição do motorista com as informações já cadastradas do banco de dados."""
    motorista = Utils.motorista(url)
    motorista = list(motorista[1:-1])

    motorista[2] = "".join(c for c in motorista[2] if str.isdigit(c))
    motorista[3] = "".join(c for c in motorista[3] if str.isdigit(c))
    
    motorista[4] = motorista[4].split("/")

    if len(motorista[4]) > 1:
        motorista.insert(5, "".join(c for c in motorista[4][1] if str.isdigit(c)))
        motorista[4] = "".join(c for c in motorista[4][0] if str.isdigit(c))
    else:
        motorista.insert(5, "")
        motorista[4] = "".join(c for c in motorista[4][0] if str.isdigit(c))

    motorista[6] = motorista[6].replace("-", "")
    motorista[-1] = motorista[-1].split("/")

    return motorista


@dash.callback(
    Output("pg3--mod1", "style"),
    Input("pg3--mod1-abrir", "n_clicks"),
    Input("pg3--mod1-backdrop", "n_clicks"),
    Input("pg3--mod1-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def forms_editar_abrir(*bt):
    """Abre o modal de formulário para edição de motoristas do banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg3--mod1-backdrop", "pg3--mod1-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg3--mod1-refresh", "refresh"),
    Output("pg3--mod1-refresh", "pathname"),
    Output("pg3--mod1-forms-feedback", "children"),
    Input("pg3--mod1-confirmar", "n_clicks"),
    State("pg3--mod1-refresh", "pathname"),
    [State(f"pg3--mod1-forms{i}", "value") for i in range(1, 15)],
    prevent_initial_call=True
    )
def forms_editar_confirmar(bt, path, *forms):
    """Confirma a edição das informações do motorista no banco de dados."""
    if bt:
        banco_dados = database.BancoDados()

        erro = Utils.filtrar(forms)
        if erro is not None:
            return *[dash.no_update] * 2, erro

        forms = list(forms)

        forms[3] = f"{forms[3][:3]}.{forms[3][3:6]}.{forms[3][6:9]}-{forms[3][9:]}"
        forms[2] = f"{forms[2][:2]}.{forms[2][2:5]}.{forms[2][5:8]}-{forms[2][-1]}"

        for rg_cpf in banco_dados.motoristas_identidade():
            if forms[3] == rg_cpf[1]:
                return *[dash.no_update] * 2, "O CPF inserido já existe no banco de dados."
            elif forms[2] == rg_cpf[0]:
                return *[dash.no_update] * 2, "O RG inserido já existe no banco de dados."

        forms[6] = f"{forms[6][:5]}-{forms[6][5:]}"
        forms[-1] = "/".join(forms[-1])

        tel2 = forms.pop(5)
        forms[4] = f"({forms[4][:2]}) {forms[4][2:-4]}-{forms[4][-4:]}"
        if tel2 not in ["", None]:
            forms[4] = f"{forms[4]} / ({tel2[:2]}) {tel2[2:-4]}-{tel2[-4:]}"

        banco_dados.motoristas_atualizar(forms)

        if path == "/motoristas/":
            return True, "/motoristas", dash.no_update
        else:
            return True, "/motoristas/", dash.no_update
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg3--mod2", "style"),
    Input("pg3--mod2-abrir", "n_clicks"),
    Input("pg3--mod2-backdrop", "n_clicks"),
    Input("pg3--mod2-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def deletar_abrir(*bt):
    """Abre o modal de confirmação para deletar o motorista selecionado do banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg3--mod2-backdrop", "pg3--mod2-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg3--mod2-refresh", "refresh"),
    Output("pg3--mod2-refresh", "pathname"),
    Output("pg3--mod2-refresh", "search"),
    Input("pg3--mod2-confirmar", "n_clicks"),
    State("pg3--mod2-confirmar", "value"),
    State("pg3--mod2-refresh", "pathname"),
    prevent_initial_call=True
    )
def deletar_confirmar(bt, cpf, path):
    """Confirma a exclusão do motorista selecionado do banco de dados."""
    if bt:
        banco_dados = database.BancoDados()
        banco_dados.motoristas_deletar(cpf)
        banco_dados.finalizar()

        img_arquivos = listdir(Utils.assets_path() + "\\assets\\images\\motoristas\\")
        img_nomes = [img.split(".")[0] for img in img_arquivos]
        if cpf in img_nomes:
            remove(f"./assets/images/motoristas/{img_arquivos[img_nomes.index(cpf)]}")

        if path == "/motoristas/":
            return True, "/motoristas", ""
        else:
            return True, "/motoristas/", ""
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg3--upload-refresh", "refresh"),
    Output("pg3--upload-refresh", "pathname"),
    Output("pg3--mod3", "style"),
    Input("pg3--mod3-backdrop", "n_clicks"),
    Input("pg3--upload", "contents"),
    State("pg3--upload", "filename"),
    State("pg3--url", "search"),
    State("pg3--upload-refresh", "pathname"),
    prevent_initial_call=True
    )
def upload_imagem(bt, img, filename, query, path):
    """Upload de imagem de motorista para o dashboard com mensagem de erro."""
    if img is not None and ctx.triggered_id == "pg3--upload":
        try:
            img = re.sub("^data:image/.+;base64,", "", img)
            img_b64 = base64.b64decode(img)
            imagem = Image.open(BytesIO(img_b64))
            imagem = imagem.resize((260, 325))
            imagem.save(f"./assets/images/motoristas/{Utils.motorista(query)[4]}.{filename.split('.')[4]}")
            if path == "/motoristas/":
                return True, "/motoristas", dash.no_update
            else:
                return True, "/motoristas/", dash.no_update
        except:
            return *[dash.no_update] * 2, {"visibility": "visible"}
    elif ctx.triggered_id == "pg3--mod3-backdrop":
        return *[dash.no_update] * 2, {"visibility": "hidden"}
    else:
        raise PreventUpdate
