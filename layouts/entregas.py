from dash import html, dcc
import pandas as pd


def entregas() -> html.Div:
    """Página de análise de entregas — rotas, custos, informações essênciais"""
    return html.Div(className="painel-entregas", children=[
        html.Div(className="box-dropdown", children=[
            html.H1("Entregas"),
            html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do banco "
                   "de dados."),
            dcc.Dropdown(className="dropdown", options=options(), value=1, clearable=False, id="entregas-dropdown"),
            dcc.Checklist(className="checklist", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                value=[True], inline=True, id="entregas-filtro")
            ]),
        html.Div(className="box-mapa-rotas", children=[
            html.H1("Rotas de Entrega"),
            dcc.Graph(className="mapa", id="entregas-mapa"),
            html.Table(className="tabela-rotas", id="entregas-tabela-rotas")
            ]),
        html.Div(className="box-informacoes", id="entregas-box-informacoes", children="Nenhuma entrega foi selecionada")
        ])


def options() -> list:
    dados = pd.read_csv("./database/_dataframe.csv", delimiter=";")
    lista_opcoes = list()
    for linha in dados.iterrows():
        linha = dict(linha[1])
        lista_opcoes.append({
            "label": f"COD#{linha['id']} - {linha['ponto_partida']} // {linha['ponto_chegada']}",
            "value": linha["id"]
            })
    return lista_opcoes
