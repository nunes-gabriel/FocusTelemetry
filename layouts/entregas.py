from dash import html, dcc

import database


def entregas() -> html.Div:
    """Página de análise de entregas — rotas, custos, informações essênciais"""
    return html.Div(id="painel-entregas", children=[
        html.Div(className="row", children=[
            html.Div(className="column", children=[
                html.Div(className="card", id="box-pesquisa", children=[
                    html.H1("Entregas"),
                    html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do"
                           "banco de dados."),
                    dcc.Dropdown(id="box-pesquisa-dropdown", options=entregas_opcoes(), value=1, clearable=False),
                    dcc.Checklist(id="box-pesquisa-filtro", options=[{"label": "Exibir entregas conclúidas", "value": True}],
                                  value=[True], inline=True)
                    ]),
                html.Div(className="card", id="box-info-geral", children=[
                    html.H1("Informações Gerais"),
                    html.Div(id="box-info-geral-textos"),
                    html.Div(className="row", children=[
                        html.Button(className="botao", id="box-info-geral-entregue", children="Marcar c/ Entregue"),
                        html.Button(className="botao", id="box-info-geral-saida", children="Saiu p/ Entrega")
                        ]),
                    ])
                ]),
            html.Div(className="card", id="box-mapa-rotas", children=[
                dcc.Graph(id="box-mapa-rotas-graph")
                ])
            ]),
        html.Div(className="card", id="box-info-rotas")
        ])


def entregas_opcoes() -> list:
    banco_dados = database.BancoDados()
    opcoes = list()
    for linha in banco_dados.entregas_lista():
        opcoes.append({
            "label": f"ID#{linha[0]} - {linha[3]} // {linha[6]} // {linha[4]}",
            "value": linha[0]
            })
    else:
        banco_dados.finalizar()
        return opcoes
