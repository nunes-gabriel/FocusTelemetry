from dash import html, dcc


class Modal(html.Div):
    def __init__(self, children=None, backdrop=True, backdrop_color=""):
        super().__init__(children=children)
