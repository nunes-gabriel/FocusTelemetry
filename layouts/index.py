from dash import html, dcc
from dash.html import Br


def index():
    """Interface base do dashboard com uma barra lateral, um espaço para exibição
    do conteúdo dos paineis do dashboard e um 'url-getter' para callback."""
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
