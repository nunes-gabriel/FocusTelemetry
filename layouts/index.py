from dash import html, dcc
from dash.html import Br


def index_layout() -> html.Div:
    """
    Interface base do Dashboard onde serão indexados os demais layouts da
    aplicação através de uma barra lateral e um 'url-getter', permitindo
    alternar entre os diferentes paineis.
    """
    return html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(className="BarraLateral", children=[
            dcc.Link(className="Botao", href="/entregas", children="Entregas"), Br(),
            dcc.Link(className="Botao", href="/veiculos", children="Veículos"), Br(),
            dcc.Link(className="Botao", href="/motoristas", children="Motoristas"), Br(),
            dcc.Link(className="Botao", href="/analise", children="Análise"), Br(),
            dcc.Link(className="Botao", href="/banco-dados", children="Banco de Dados")
            ]),
        html.Div(id="conteudo-pagina")
        ])
