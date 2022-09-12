from dash import html, dcc


def index_layout() -> html.Div:
    """
    Interface base do Dashboard onde serão indexados os demais layouts da
    aplicação através de uma barra lateral e um 'url-getter', permitindo
    alternar entre os diferentes paineis.
    """
    return html.Div(
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(
                className="barra-lateral",
                children=[
                    dcc.Link(
                        className="botao",
                        title="Início",
                        href="/",
                        children=html.Img(
                            className="icone",
                            src="./assets/rosa-dos-ventos.png",
                            width="50px", height="50px"
                            )
                        ),
                    html.Br(),
                    dcc.Link(
                        className="botao",
                        title="Entregas",
                        href="/entregas",
                        children=html.Img(
                            className="icone",
                            src="./assets/icone-entregas.svg",
                            width="50px", height="50px"
                            )
                        ),
                    html.Br(),
                    dcc.Link(
                        className="botao",
                        title="Veículos",
                        href="/veiculos",
                        children=html.Img(
                            className="icone",
                            src="./assets/icone-veiculos.svg",
                            width="50px", height="50px"
                            )
                        ),
                    html.Br(),
                    dcc.Link(
                        className="botao",
                        title="Motoristas",
                        href="/motoristas",
                        children=html.Img(
                            className="icone",
                            src="./assets/icone-motoristas.svg",
                            width="50px", height="50px"
                            )
                        ),
                    html.Br(),
                    dcc.Link(
                        className="botao",
                        title="Análise Geral",
                        href="/analise",
                        children=html.Img(
                            className="icone",
                            src="./assets/icone-analise.svg",
                            width="50px", height="50px"
                            )
                        ),
                    html.Br(),
                    dcc.Link(
                        className="botao",
                        title="Banco de Dados",
                        href="/banco-dados",
                        children=html.Img(
                            className="icone",
                            src="./assets/icone-banco-dados.svg",
                            width="50px", height="50px"
                            )
                        )
                    ]
                ),
            html.Div(
                className="conteudo-pagina",
                id="conteudo-pagina"
                )
            ]
        )
