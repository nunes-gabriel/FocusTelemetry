from dash import html, dcc


def banco_dados_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(
        className="painel-banco-dados",
        children=[
            html.H1("Banco de Dados")
            ]
        )