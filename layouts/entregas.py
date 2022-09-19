from dash import html, dcc
import pandas as pd


def entregas() -> html.Div:
    """Página de análise de entregas — rotas, custos, informações essênciais"""
    return html.Div(id="painel-entregas", children=[
        html.Div(className="row", children=[
            html.Div(className="column", children=[
                html.Div(id="box-pesquisa", children=[
                    html.H1("Entregas"),
                    html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do"
                           "banco de dados."),
                    dcc.Dropdown(id="box-pesquisa-dropdown", options=entregas_opcoes(), value=1, clearable=False),
                    dcc.Checklist(id="box-pesquisa-filtro", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                                  value=[True], inline=True)
                    ]),
                html.Div(id="box-info-geral", children=[
                    html.H1("Informações Gerais"),
                    html.Div(id="box-info-geral-textos"),
                    html.Div(className="row", children=[
                        html.Button(className="botao", id="box-info-geral-entregue", children="Marcar c/ Entregue"),
                        html.Button(className="botao", id="box-info-geral-saida", children="Saiu p/ Entrega")
                        ]),
                    ])
                ]),
            html.Div(id="box-rotas", children=[
                html.H1("Rotas de Viagem"),
                dcc.Graph(id="box-rotas-mapa"),
                html.Table(id="box-rotas-tabela")
                ])
            ])
        ])


def entregas_opcoes() -> list:
    dados = pd.read_csv("./database/_dataframe.csv", delimiter=";")
    lista_opcoes = list()
    for linha in dados.iterrows():
        linha = dict(linha[1])
        lista_opcoes.append({
            "label": f"COD#{linha['id']} - {linha['ponto_partida']} // {linha['ponto_chegada']}",
            "value": linha["id"]
            })
    return lista_opcoes
