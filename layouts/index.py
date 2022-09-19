from dash import html, dcc


def index() -> html.Div:
    """
    Interface base do Dashboard onde serão indexados os demais layouts da
    aplicação através de uma barra lateral e um 'url-getter', permitindo
    alternar entre os diferentes paineis.
    """
    return html.Div(children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="barra-lateral", children=[
            dcc.Link(title="Início", href="/", children=html.Img(
                src="./assets/icone-home.svg", width="40px", height="40px"
                )),
            html.Br(),
            dcc.Link(title="Entregas", href="/entregas", children=html.Img(
                src="./assets/icone-entregas.svg", width="40px", height="40px"
                )),
            html.Br(),
            dcc.Link(title="Veículos", href="/veiculos", children=html.Img(
                src="./assets/icone-veiculos.svg", width="40px", height="40px"
                )),
            html.Br(),
            dcc.Link(title="Motoristas", href="/motoristas", children=html.Img(
                src="./assets/icone-motoristas.svg", width="40px", height="40px"
                )),
            html.Br(),
            dcc.Link(title="Análise Geral", href="/analise", children=html.Img(
                src="./assets/icone-analise.svg", width="40px", height="40px"
                )),
            html.Br(),
            dcc.Link(title="Banco de Dados", href="/banco-dados", children=html.Img(
                src="./assets/icone-banco-dados.svg", width="40px", height="40px"
                ))
            ]),
        html.Div(id="conteudo-pagina")
        ])
