from dash import html, dcc
from dash.html import Br


def entregas_layout() -> html.Div:
    """
    Painel de entregas da transportadora contendo informações e análises sobre
    cada uma das viagens registradas no banco de dados - tempo de viagem, rotas
    alternativas, custos totais, mapa interativo com pontos de entrega, etc.
    """
    return html.Div(className="painel-entregas", children=[
        html.Div(className="box-escolha", children=[
            html.H1("Entregas"),
            html.P("Escolha uma entrega para análise. Caso queira registrar uma nova entrega acesse o painel do banco de dados."),
            dcc.Dropdown(id="dropdown-entregas")
            ]),
        html.Div(className="box-mapa", children=[
            html.H2("Rotas de Entrega"),
            dcc.Graph(className="mapa", id="mapa-entregas")
            ]),
        html.Div(className="box-infos", children=[
            html.H2("Informações")
            ]),
        html.Div(className="box-analise", children=[
            html.H2("Análise")
            ])
        ])


def index_layout() -> html.Div:
    """
    Interface base do Dashboard onde serão indexados os demais layouts da
    aplicação através de uma barra lateral e um 'url-getter', permitindo
    alternar entre os diferentes paineis.
    """
    return html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(className="barra-lateral", children=[
            dcc.Link(className="botao", title="Entregas", href="/", children=html.Img(className="icone", src="./assets/icone-entregas.svg", width="50px", height="50px")), Br(),
            dcc.Link(className="botao", title="Veículos", href="/veiculos", children=html.Img(className="icone", src="./assets/icone-veiculos.svg", width="50px", height="50px")), Br(),
            dcc.Link(className="botao", title="Motoristas", href="/motoristas", children=html.Img(className="icone", src="./assets/icone-motoristas.svg", width="50px", height="50px")), Br(),
            dcc.Link(className="botao", title="Análise Geral", href="/analise", children=html.Img(className="icone", src="./assets/icone-analise.svg", width="50px", height="50px")), Br(),
            dcc.Link(className="botao", title="Banco de Dados", href="/banco-dados", children=html.Img(className="icone", src="./assets/icone-banco-dados.svg", width="50px", height="50px"))
            ]),
        html.Div(className="page-layer", id="conteudo-pagina")
        ])
