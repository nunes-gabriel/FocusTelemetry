from dash import html, dcc


def motoristas_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(
        className="painel-motoristas",
        children=[
            html.H1("Motoristas")
            ]
        )
