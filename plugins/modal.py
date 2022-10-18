from dash import html, dcc


class Modal(html.Div):
    def __init__(self, children=None, className=None, id=None, backdrop_color="#00000063"):
        content_layout = [
            html.Button(n_clicks=0, style={
                "background-color": backdrop_color,
                "position": "absolute",
                "border": "none",
                "height": "100%",
                "width": "100%",
                "top": "0",
                "left": "0",
                "z-index": "100",
                "display": "none"
                }),
            html.Div(className=className, id=id, children=children)
            ]

        super().__init__(children=content_layout)
