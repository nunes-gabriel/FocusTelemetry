from dash import html, dcc
from dash.html import Br


def index():
    """Página de indexação contendo um menu para os demais paineis do app."""
    return html.Div(className="page-index", children=[
        html.Div(className="menu-index", children=[
            html.Img(className="logo", src="/assets/logo-entra21.png", width="10%", height="10%"), Br(),
            dcc.Link(className="botao", href="/entregas", children="Entregas"), Br(),
            dcc.Link(className="botao", href="/veiculos", children="Veículos"), Br(),
            dcc.Link(className="botao", href="/motoristas", children="Motoristas"), Br(),
            dcc.Link(className="botao", href="/analise", children="Análise"), Br(),
            dcc.Link(className="botao", href="/banco-dados", children="Banco de Dados")
            ])
        ])
