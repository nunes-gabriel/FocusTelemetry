from dash import html, dcc


def veiculos_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(
        className="painel-veiculos",
        children=[
            html.H1("Veículos")
            ]
        )
