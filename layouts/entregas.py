from dash import html, dcc
import pandas as pd


def entregas() -> html.Div:
    """
    Painel de entregas da transportadora contendo informações e análises sobre
    cada uma das viagens registradas no banco de dados - tempo de viagem, rotas
    alternativas, custos totais, mapa interativo com pontos de entrega, etc.
    """
    entregas_csv = pd.read_csv("./database/_dataframe.csv", sep=",,,", engine="python")
    lista_entregas = list()
    for row in entregas_csv.iterrows():
        value = f"COD#{row[1]['cod_entrega']} - " \
                f'"{row[1]["ponto_partida"]}" / ' \
                f'"{row[1]["ponto_chegada"]}"'
        lista_entregas.append(value)

    return html.Div(className="painel-entregas", children=[
        html.Div(className="box-dropdown", children=[
            html.H1("Entregas"),
            html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do banco de dados."),
            dcc.Dropdown(className="dropdown", options=lista_entregas, value=lista_entregas[0], id="entregas-dropdown")
            ]),
        html.Div(className="box-mapa-rotas", children=[
            html.H1("Rotas de Entrega"),
            dcc.Graph(className="mapa", id="entregas-mapa"),
            html.Table(className="tabela-rotas", id="entregas-tabela-rotas")
            ]),
        html.Div(className="box-informacoes", id="entregas-box-informacoes", children="Nenhuma entrega foi selecionada")
        ])
