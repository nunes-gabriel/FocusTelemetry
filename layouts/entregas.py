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
                    html.P(id="box-info-geral-output-botoes")
                    ])
                ]),
            html.Div(className="card", id="box-rotas", children=[
                dcc.Graph(id="box-rotas-mapa"),
                html.Div(className="card", id="box-rotas-tabelas")
                ])
            ])
        ])


def entregas_opcoes() -> list:
    banco_dados = database.BancoDados()
    opcoes = list()
    for linha in banco_dados.entregas_lista():
        label_meio = "//"
        if linha[8] != "Sem parada ":
            paradas = linha[8].split("/")
            if len(paradas) > 2:
                label_meio += f" {paradas[0]} // ... // {paradas[-1]}  //"
            else:
                for parada in paradas:
                    label_meio += f" {parada} //"
        opcoes.append({
            "label": f"ID#{linha[0]} - {linha[3]} {label_meio} {linha[4]}",
            "value": linha[0]
            })
    else:
        banco_dados.finalizar()
        return opcoes
