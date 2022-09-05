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
        html.Div(className="barra-lateral", children=[
            dcc.Link(className="botao", href="/entregas", children=html.Img(className="icone", src="./assets/icone-entregas.svg", width="60px", height="60px")), Br(),
            dcc.Link(className="botao", href="/veiculos", children=html.Img(className="icone", src="./assets/icone-veiculos.svg", width="60px", height="60px")), Br(),
            dcc.Link(className="botao", href="/motoristas", children=html.Img(className="icone", src="./assets/icone-motoristas.svg", width="60px", height="60px")), Br(),
            dcc.Link(className="botao", href="/analise", children=html.Img(className="icone", src="./assets/icone-analise.svg", width="60px", height="60px")), Br(),
            dcc.Link(className="botao", href="/banco-dados", children=html.Img(className="icone", src="./assets/icone-banco-dados.svg", width="60px", height="60px"))
            ]),
        html.Div(className="page-layer", id="conteudo-pagina")
        ])
