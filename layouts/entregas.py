from dash import html, dcc
import plotly.express as px


def entregas_layout() -> html.Div:
    """
    Painel de entregas da transportadora contendo informações e análises sobre
    cada uma das viagens registradas no banco de dados - tempo de viagem, rotas
    alternativas, custos totais, mapa interativo com pontos de entrega, etc.
    """
    return html.Div(
        className="painel-entregas",
        children=[
            html.Div(
                className="box-dropdown",
                children=[
                    html.H1("Entregas"),
                    html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do banco de dados."),
                    dcc.Dropdown(id="dropdown-entregas")
                    ]
                ),
            html.Div(
                className="box-mapa-rotas",
                children=[
                    html.H2("Rotas de Entrega"),
                    dcc.Graph(
                        className="mapa-entregas",
                        id="mapa-entregas"
                        )
                    ]
                ),
            html.Div(
                className="box-informacoes",
                id="box-informacoes",
                children="Nenhuma entrega foi selecionada"
                )
            ]
        )
