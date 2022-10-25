from dash import html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from plotly import graph_objects as go
from os import remove

import os
import datetime
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


def layout(**query):
    return html.Div(children=[
        dcc.Location(id="pg1--url", refresh=False),
        dcc.Graph(id="pg1--mapa"),
        html.Div(id="pg1--mapa-fadeout"),
        html.Div(className="card search-A", children=[
            html.H1("Entregas"),
            html.P("Escolha uma entrega para análise ou cadastre uma nova entrega no sistema."),
            html.Div(className="row search-A", children=[
                dcc.Dropdown(className="dropdown search-A", id="pg1--dropdown", value=query.get("id", 1), clearable=False),
                html.Button(className="button-search click", n_clicks=0, id="pg1--mod0-abrir", children=html.Img(
                    src=dash.get_asset_url("icons/icone-adicionar.svg"), width="34px", height="34px"
                    ))
                ]),
            dcc.Checklist(className="checklist search-A", id="pg1--checklist", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                value=[True], inline=True)
            ]),
        html.Div(className="card infos-A", children=[
            html.H1("Informações"),
            html.Div(className="infos-list", id="pg1--informacoes"),
            html.H2("Paradas"),
            html.Table(id="pg1--tabela"),
            html.Button(className="button infos-A click", n_clicks=0, id="pg1--botao-entregue", children="Marcar como entregue"),
            html.Br(),
            html.Button(className="button infos-A click", n_clicks=0, id="pg1--botao-saida", children="Saiu para entrega"),
            html.Div(className="buttons-layout", children=[
                html.Button(className="button-infos-A last click", n_clicks=0, id="pg1--mod1-abrir", children=html.Img(
                    src=dash.get_asset_url("icons/icone-lixeira.svg"), width="22.5px", height="22.5px"
                    ))
                ]),
            ]),
        html.Div(id="pg1--mapa-legenda", children=[
            html.Label([html.Span(className="circulo ponto--partida"), "Ponto de Partida"]),
            html.Label([html.Span(className="circulo ponto--parada"), "Ponto de Parada"]),
            html.Label([html.Hr(className="linha rota--recomendada"), "Rota Recomendada"]),
            html.Label([html.Hr(className="linha rota--alternativas"), "Rota Alternativa"])
            ]),
        html.Div(className="modal-div", children=[
            Layouts.forms(),
            Layouts.deletar(),
            Layouts.entregue(),
            Layouts.aviso_entregue(),
            Layouts.saiu(),
            Layouts.aviso_saida(),
            ])
        ])


class Layouts:
    @staticmethod
    def forms():
        """Modal para cadastro e edição de entregas no banco de dados."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id=f"pg1--mod0", children=[
            dcc.Location(id=f"pg1--mod0-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id=f"pg1--mod0-backdrop"),
            html.Div(className="card modal-body", id=f"pg1--mod0-conteudo", children=[
                html.H1("Registrar Entrega"),
                html.Form(className="modal-form", children=[
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Veículo"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, options=Utils.veiculos(), value=Utils.veiculos_value(), id=f"pg1--mod0-forms1"),
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Motorista"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, options=Utils.motoristas(), value=Utils.motoristas_value(), id=f"pg1--mod0-forms2"),
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-dropdown", children="Tipo de Carga"),
                            dcc.Dropdown(className="form-field dropdown", clearable=False, id=f"pg1--mod0-forms5", value="Carga de Valor", options=[
                                {"label": "Carga de Valor", "value": "Carga de Valor"},
                                {"label": "Carga de Veículos", "value": "Carga de Veículos"},
                                {"label": "Carga Seca", "value": "Carga Seca"},
                                {"label": "Carga Viva", "value": "Carga Viva"},
                                {"label": "Carga de Medicamentos", "value": "Carga de Medicamentos "},
                                {"label": "Carga Frigorificada", "value": "Carga Frigorificada"},
                                {"label": "Carga Frigorificada (Perigosa)", "value": "Carga Frigorificada (Perigosa)"},
                                {"label": "Carga Neogranel", "value": "Carga Neogranel "},
                                {"label": "Carga Granel: Sólida", "value": "Carga Granel: Sólida"},
                                {"label": "Carga Granel: Sólida (Perigosa)", "value": "Carga Granel: Sólida (Perigosa)"},
                                {"label": "Carga Granel: Líquido", "value": "Carga Granel: Líquido "},
                                {"label": "Carga Granel: Líquido (Perigosa)", "value": "Carga Granel: Líquido (Perigosa)"},
                                {"label": "Carga Refrigerada: Congelados", "value": "Carga Refrigerada: Congelados"},
                                {"label": "Carga Perigosa (conteinerizada)", "value": " Carga Perigosa (conteinerizada)"},
                                {"label": "Carga de Minério e Cimento", "value": "Carga de Minério e Cimento"}
                                ])
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Quantidade(kg)"),
                            dcc.Input(className="input", type="number", id=f"pg1--mod0-forms6")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Valor da Carga"),
                            dcc.Input(className="input", type="number", id=f"pg1--mod0-forms7")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-datepicker", children="Data de Saída"),
                            dcc.DatePickerSingle(className="form-field datepicker", display_format="DD/MM/YYYY", id=f"pg1--mod0-forms9")])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Ponto de Partida"),
                            dcc.Input(className="input", type="text", id=f"pg1--mod0-forms3")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span("Ponto de Chegada"),
                            dcc.Input(className="input", type="text", id=f"pg1--mod0-forms4")
                            ])
                        ]),
                    html.Div(className="row form-field", children=[
                        html.Label([
                            html.Span(className="span-textarea", children="Pontos de Parada"),
                            dcc.Textarea(className="textarea", required=False, draggable=False, spellCheck=False, id=f"pg1--mod0-forms8")
                            ])
                        ])
                    ]),
                html.Div(style={"color": "red", "font-size": "11px"}, id=f"pg1--mod0-forms-feedback"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id=f"pg1--mod0-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id=f"pg1--mod0-cancelar", children="Cancelar")
                    ])
                ])
            ])

    @staticmethod
    def deletar():
        """Modal para confirmação de deletar entrega."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg1--mod1", children=[
            dcc.Location(id="pg1--mod1-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id="pg1--mod1-backdrop"),
            html.Div(className="card modal-body", id="pg1--mod1-conteudo", children=[
                html.H3(style={"margin-top": "15px"}, children="Tem certeza que deseja deletar a entrega do banco de dados?"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id="pg1--mod1-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id="pg1--mod1-cancelar", children="Cancelar"),
                    ])
                ])
            ])

    @staticmethod
    def entregue():
        """Modal para confirmar entrega."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg1--mod2", children=[
            dcc.Location(id="pg1--mod2-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id="pg1--mod2-backdrop"),
            html.Div(className="card modal-body", id="pg1--mod2-conteudo", children=[
                html.H3(style={"margin-top": "15px"}, children="Tem certeza que deseja marcar a viagem como entregue?"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id="pg1--mod2-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id="pg1--mod2-cancelar", children="Cancelar"),
                    ])
                ])
            ])

    @staticmethod
    def saiu():
        """Modal para confirmar saída do veículo."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg1--mod3", children=[
            dcc.Location(id="pg1--mod3-refresh", refresh=False),
            html.Button(className="modal-backdrop", n_clicks=0, id="pg1--mod3-backdrop"),
            html.Div(className="card modal-body", id="pg1--mod3-conteudo", children=[
                html.H3(style={"margin-top": "15px"}, children="Confirmar a saída do veículo para entrega?"),
                html.Div(className="row form-buttons", children=[
                    html.Button(className="button form-button click", n_clicks=0, id="pg1--mod3-confirmar", children="Confirmar"),
                    html.Button(className="button form-button click", n_clicks=0, id="pg1--mod3-cancelar", children="Cancelar"),
                    ])
                ])
            ])

    @staticmethod
    def aviso_entregue():
        """Aviso de erro para o botão de marcar para entrega."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg1--mod4", children=[
            html.Button(className="modal-backdrop", n_clicks=0, id="pg1--mod4-backdrop"),
            html.Div(className="card modal-body", id="pg1--mod4-conteudo", children=[
                html.H3(style={"margin-top": "15px", "margin-bottom": "15px"}, id="pg1--mod4-aviso")
                ])
            ])

    @staticmethod
    def aviso_saida():
        """Aviso de erro para o botão de saiu para entrega."""
        return html.Div(className="modal", style={"visibility": "hidden"}, id="pg1--mod5", children=[
            html.Button(className="modal-backdrop", n_clicks=0, id="pg1--mod5-backdrop"),
            html.Div(className="card modal-body", id="pg1--mod5-conteudo", children=[
                html.H3(style={"margin-top": "15px", "margin-bottom": "15px"}, id="pg1--mod5-aviso")
                ])
            ])


class Utils:
    @staticmethod
    def assets_path():
        return os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)

    @staticmethod
    def veiculos():
        banco_dados = database.BancoDados()
        veiculos = banco_dados.veiculos_disponiveis()
        banco_dados.finalizar()
        return [
            {"label": f"{veiculo[0]} - {veiculo[1]}", "value": veiculo[0]}
            for veiculo in veiculos
            ]

    @staticmethod
    def veiculos_value():
        banco_dados = database.BancoDados()
        veiculos = banco_dados.veiculos_disponiveis()
        banco_dados.finalizar()
        return veiculos[0][0]

    @staticmethod
    def motoristas():
        banco_dados = database.BancoDados()
        motoristas = banco_dados.motoristas_disponiveis()
        banco_dados.finalizar()
        return [
            {"label": f"{motorista[0]} - {motorista[1]}", "value": motorista[1]}
            for motorista in motoristas
            ]

    @staticmethod
    def motoristas_value():
        banco_dados = database.BancoDados()
        motoristas = banco_dados.motoristas_disponiveis()
        banco_dados.finalizar()
        return motoristas[0][1]

    @staticmethod
    def filtrar(forms: tuple):
        """Filtra os formulários de cadastro e edição para evitar erros no banco de dados."""
        if any(form in [None, "", 0] for form in forms[:7]):
            return "Um dos campos do formulários está vazio ou com um valor inválido."
        elif forms[-1] not in [None, ""]:
            try:
                ano, mes, dia = [int(d) for d in forms[-1].split("-")]
                datetime.date(ano, mes, dia)
            except Exception as err:
                return str(err) #"A data de saída inserida é inválida."
        return None
    
    @staticmethod
    def data_prevista(tempo_total: int, data_saida: str):
        """Calcula a data prevista de chegada da entrega a partir do tempo total de viagem"""
        dias = int(tempo_total / 3600 / 8) + 1
        ano, mes, dia = [int(d) for d in data_saida.split("-")]
        data = datetime.date(ano, mes, dia) + datetime.timedelta(days=dias)
        return f"{data.day}/{data.month}/{data.year}"


@dash.callback(
    Output("pg1--mapa", "figure"),
    Output("pg1--informacoes", "children"),
    Output("pg1--tabela", "children"),
    Input("pg1--dropdown", "value"),
    )
def dropdown_callbacks(id_entrega: int):
    maps = plugins.maps.GoogleMaps(cod_entrega=id_entrega)
    
    banco_dados = database.BancoDados()
    dados_entrega = banco_dados.entregas_busca(id_entrega)
    banco_dados.finalizar()

    def mapa_figure():
        mapa = go.Figure()
        rota_final = None

        def _LINHAS():
            nonlocal mapa
            for index, rota in enumerate(reversed(maps.rota_dataframe)):
                mapa.add_trace(go.Scattermapbox(
                    mode="lines",
                    lon=rota["linhas"]["lon"],
                    lat=rota["linhas"]["lat"],
                    name=rota["linhas"]["nome"],
                    hoverinfo="skip",
                    line={
                        "color": "#1f448e" if index != len(maps.rota_dataframe) - 1 else "#df2929",
                        "width": 3
                        }
                    ))
            else:
                nonlocal rota_final
                rota_final = rota

        def _PARADAS():
            nonlocal mapa
            mapa.add_trace(go.Scattermapbox(
                mode="markers",
                lon=rota_final["pontos"]["lon"],
                lat=rota_final["pontos"]["lat"],
                name="Parada",
                marker={
                    "size": 14,
                    "color": "#f0e43a"
                    }
                ))

        def _PARTIDA():
            nonlocal mapa
            mapa.add_trace(go.Scattermapbox(
                mode="markers",
                lon=[rota_final["pontos"]["partida"]["lon"]],
                lat=[rota_final["pontos"]["partida"]["lat"]],
                name="Partida",
                marker={
                    "size": 14,
                    "color": "#1C1C1C"
                    }
                ))

        def _LAYOUT():
            nonlocal mapa
            mapa.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                mapbox={
                    "center": {"lon": -53.1805017, "lat": -14.2400732},
                    "style": "carto-positron",
                    "zoom": 4
                    },
                paper_bgcolor="#D4DADC"
                ) \
            .update_traces(showlegend=False)

        _LINHAS()
        _PARADAS()
        _PARTIDA()
        _LAYOUT()

        return mapa

    def informacoes_children():
        return [
            html.P(f"ID da Entrega: {id_entrega}"),
            html.P(id="pg1--infos-status", children=f"Status Atual: {dados_entrega[-2]}"),
            html.P(id="pg1--infos-feedback", children=f"Feedback: {dados_entrega[-1]}"),
            html.P(id="pg1--infos-data-saida", children=f"Data de Saída: {dados_entrega[9]}"),
            html.P(id="pg1--infos-data-prevista", children=f"Previsão de Entrega: {dados_entrega[10]}"),
            html.P(id="pg1--infos-data-chegada", children=f"Data de Chegada: {dados_entrega[11]}"),
            html.Hr(),
            html.P(children=[
                "Placa do Veículo: ",
                dcc.Link(href=f"/veiculos?placa={dados_entrega[1]}", target="_blank", children=dados_entrega[1])
                ]),
            html.P(children=[
                "CPF do Motorista: ",
                dcc.Link(href=f"/motoristas?cpf={dados_entrega[2]}", target="_blank", children=dados_entrega[2])
                ]),
            html.P(f"Tipo de Carga: {dados_entrega[5]}"),
            html.P(f"Peso da Carga: {dados_entrega[6]}kg"),
            html.P(f"Valor da Carga: R${dados_entrega[7]}")
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
    Output("pg1--dropdown", "options"),
    Input("pg1--checklist", "value")
    )
def filtrar_entregas(filtro: bool):
    banco_dados = database.BancoDados()
    opcoes = list()
    for linha in banco_dados.entregas_lista():
        if not filtro and linha[-2] in ["Entregue", "Entregue "]:
            continue
        label_meio = "|"
        if linha[8] != "Sem parada ":
            paradas = linha[8].split("/")
            if len(paradas) > 2:
                label_meio += f" {paradas[0]} | ... | {paradas[-1]}  |"
            else:
                for parada in paradas:
                    label_meio += f" {parada} |"
        opcoes.append({
            "label": f"ID#{linha[0]} - {linha[3]} {label_meio} {linha[4]}",
            "value": linha[0]
        })
    else:
        banco_dados.finalizar()
        return opcoes


@dash.callback(
    Output("pg1--mod0", "style"),
    Input("pg1--mod0-abrir", "n_clicks"),
    Input("pg1--mod0-backdrop", "n_clicks"),
    Input("pg1--mod0-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def forms_novo_abrir(*bt):
    """Abre o modal de formulário para cadastro de entregas no banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg1--mod0-backdrop", "pg1--mod0-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg1--mod0-refresh", "refresh"),
    Output("pg1--mod0-refresh", "pathname"),
    Output("pg1--mod0-refresh", "search"),
    Output("pg1--mod0-forms-feedback", "children"),
    Input("pg1--mod0-confirmar", "n_clicks"),
    State("pg1--mod0-refresh", "pathname"),
    [State(f"pg1--mod0-forms{i}", "value") for i in range(1, 9)],
    State("pg1--mod0-forms9", "date"),
    prevent_initial_call=True
    )
def forms_novo_confirmar(bt, path, *forms):
    """Registra um veículo no banco de dados com os dados inseridos no formulário."""
    if bt:
        banco_dados = database.BancoDados()

        erro = Utils.filtrar(forms)
        if erro is not None:
            return *[dash.no_update] * 3, erro

        forms = list(forms)
    
        if forms[-2] not in [None, ""]:
            forms[-2] = [end for end in forms[-2].splitlines() if end != ""]
        else:
            forms[-2] = []

        cadastro = plugins.maps.GoogleMaps(
            origem=forms[2],
            destino=forms[3],
            paradas=forms[-2]
            )

        if cadastro.erro:
            return *[dash.no_update] * 3, cadastro.erro

        if forms[-2] in [None, "", []]:
            forms[-2] = "Sem parada "
        else:
            forms[-2] = " / ".join(forms[-2])

        if forms[-1] not in [None, ""]:
            data_prevista = Utils.data_prevista(cadastro.rota_organizada[0]["duração"], forms[-1])
            ano, mes, dia = forms[-1].split("-")
            forms[-1] = f"{dia}/{mes}/{ano}"
        else:
            data_prevista = f"{int(cadastro.rota_organizada[0]['duração'] / 3600 / 8) + 1} dias de viagem"
            forms[-1] = "..."

        forms += [data_prevista, "...", "Não Entregue", "No Prazo"]

        id_entrega = banco_dados.entregas_id()

        banco_dados.entregas_criar(forms)
        banco_dados.entregas_ocupar(id_entrega)

        banco_dados.finalizar()

        if path == "/entregas/":
            return True, "/entregas", f"id={id_entrega}", dash.no_update
        else:
            return True, "/entregas/", f"id={id_entrega}", dash.no_update
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg1--mod1", "style"),
    Input("pg1--mod1-abrir", "n_clicks"),
    Input("pg1--mod1-backdrop", "n_clicks"),
    Input("pg1--mod1-cancelar", "n_clicks"),
    prevent_initial_call=True
    )
def deletar_abrir(*bt):
    """Abre o modal de confirmação para deletar a entrega selecionada do banco de dados."""
    if any(bt):
        if ctx.triggered_id in ["pg1--mod1-backdrop", "pg1--mod1-cancelar"]:
            return {"visibility": "hidden"}
        else:
            return {"visibility": "visible"}
    else:
        return dash.no_update


@dash.callback(
    Output("pg1--mod1-refresh", "refresh"),
    Output("pg1--mod1-refresh", "pathname"),
    Output("pg1--mod1-refresh", "search"),
    Input("pg1--mod1-confirmar", "n_clicks"),
    State("pg1--dropdown", "value"),
    State("pg1--mod1-refresh", "pathname"),
    prevent_initial_call=True
    )
def deletar_confirmar(bt, id_entrega, path):
    """Confirma a exclusão da entrega selecionada do banco de dados."""
    if bt:
        banco_dados = database.BancoDados()
        banco_dados.entregas_desocupar(int(id_entrega))
        banco_dados.entregas_deletar(int(id_entrega))
        banco_dados.finalizar()
        os.remove(Utils.assets_path() + f"\\plugins\\cache\\maps\\maps_ID#{id_entrega}.json")
        if path == "/entregas/":
            return True, "/entregas", ""
        else:
            return True, "/entregas/", ""
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg1--mod2", "style"),
    Output("pg1--mod4", "style"),
    Output("pg1--mod4-aviso", "children"),
    Output("pg1--infos-status", "children"),
    Output("pg1--infos-feedback", "children"),
    Output("pg1--infos-data-chegada", "children"),
    State("pg1--dropdown", "value"),
    Input("pg1--botao-entregue", "n_clicks"),
    Input("pg1--mod2-confirmar", "n_clicks"),
    Input("pg1--mod2-backdrop", "n_clicks"),
    Input("pg1--mod2-cancelar", "n_clicks"),
    Input("pg1--mod4-backdrop", "n_clicks"),
    prevent_initial_call=True
    )
def entregue(id_entrega, *bt):
    """Modal de confirmação de entrega da viagem."""
    if any(bt):
        if ctx.triggered_id in ["pg1--mod2-backdrop", "pg1--mod2-cancelar"]:
            return {"visibility": "hidden"}, *[dash.no_update] * 5
        elif ctx.triggered_id == "pg1--mod4-backdrop":
            return dash.no_update, {"visibility": "hidden"}, *[dash.no_update] * 4
        elif ctx.triggered_id == "pg1--mod2-confirmar":
            banco_dados = database.BancoDados()
            banco_dados.entregas_desocupar(id_entrega)
            dados = banco_dados.entregas_busca(id_entrega)

            data_prevista = [int(d) for d in dados[10].split("/")]
            data_prevista = datetime.date(data_prevista[2], data_prevista[1], data_prevista[0])
            data_chegada = datetime.datetime.today()
            data_chegada_date = datetime.date(data_prevista.year, data_prevista.month, data_prevista.day)
            data_chegada_str = f"{data_chegada.day}/{data_chegada.month}/{data_chegada.year}"

            feedback = "Entregue no Prazo"
            if data_chegada_date > data_prevista:
                feedback = "Entregue com Atraso"

            banco_dados.entregas_data_chegada(id_entrega, data_chegada_str)
            banco_dados.entregas_feedback(id_entrega, feedback)
            banco_dados.entregas_status(id_entrega, "Entregue")

            banco_dados.finalizar()
            return {"visibility": "hidden"}, *[dash.no_update] * 2, f"Status Atual: Entregue", f"Feedback: {feedback}", f"Data de Chegada: {data_chegada_str}"
        else:
            banco_dados = database.BancoDados()
            dados = banco_dados.entregas_busca(id_entrega)
            banco_dados.finalizar()
            if dados[-2] in ["Entregue", "Entregue "]:
                return dash.no_update, {"visibility": "visible"}, "A entrega em questão já foi concluída.", *[dash.no_update] * 3
            elif dados[9] == "...":
                return dash.no_update, {"visibility": "visible"}, "A entrega em questão ainda não saiu para viagem.", *[dash.no_update] * 3
            else:
                return {"visibility": "visible"}, *[dash.no_update] * 5
    else:
        raise PreventUpdate


@dash.callback(
    Output("pg1--mod3", "style"),
    Output("pg1--mod5", "style"),
    Output("pg1--mod5-aviso", "children"),
    Output("pg1--infos-data-saida", "children"),
    Output("pg1--infos-data-prevista", "children"),
    State("pg1--dropdown", "value"),
    Input("pg1--botao-saida", "n_clicks"),
    Input("pg1--mod3-confirmar", "n_clicks"),
    Input("pg1--mod3-backdrop", "n_clicks"),
    Input("pg1--mod3-cancelar", "n_clicks"),
    Input("pg1--mod5-backdrop", "n_clicks"),
    prevent_initial_call=True
    )
def saiu(id_entrega, *bt):
    """Modal de confirmação de saída do veículo."""
    if any(bt):
        if ctx.triggered_id in ["pg1--mod3-backdrop", "pg1--mod3-cancelar"]:
            return {"visibility": "hidden"}, *[dash.no_update] * 4
        elif ctx.triggered_id == "pg1--mod5-backdrop":
            return dash.no_update, {"visibility": "hidden"}, *[dash.no_update] * 3
        elif ctx.triggered_id == "pg1--mod3-confirmar":
            banco_dados = database.BancoDados()
            dados = banco_dados.entregas_busca(id_entrega)
            data = datetime.datetime.today()
            data_str2 = f"{data.day}/{data.month}/{data.year}"
            if dados[9] == "...":
                maps = plugins.maps.GoogleMaps(cod_entrega=id_entrega)
                data_str1 = f"{data.year}-{data.month}-{data.day}"
                data_prevista = Utils.data_prevista(maps.rota_organizada[0]['duração'], data_str1)
                banco_dados.entregas_data_prevista(id_entrega, data_prevista)
                banco_dados.entregas_data_saida(id_entrega, data_str2)
                banco_dados.finalizar()
                return {"visibility": "hidden"}, *[dash.no_update] * 2, f"Data de Saída: {data_str2}", f"Previsão de Entrega: {data_prevista}"
            else:
                banco_dados.entregas_data_saida(id_entrega, data_str2)
                banco_dados.finalizar()
                return {"visibility": "hidden"}, *[dash.no_update] * 2, f"Data de Saída: {data_str2}", dash.no_update
        else:
            banco_dados = database.BancoDados()
            dados = banco_dados.entregas_busca(id_entrega)
            banco_dados.finalizar()
            if dados[-2] in ["Entregue", "Entregue "]:
                return dash.no_update, {"visibility": "visible"}, "A entrega em questão já foi concluída.", *[dash.no_update] * 2
            else:
                return {"visibility": "visible"}, *[dash.no_update] * 4
    else:
        raise PreventUpdate
