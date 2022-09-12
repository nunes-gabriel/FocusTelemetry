from dash import html, dcc


def home_layout() -> html.Div:
    """
    Adicionar descrição...
    """
    return html.Div(
        className="home-site",
        children=[
            html.H1("Home")
            ]
        )
