from dash import Dash, html, dcc

import dash

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Focus Telemetry",
    update_title="Carregando..."
    )

app.layout = html.Div([
    html.Div(style={"display": "none"}, id="none"),
    html.Ul(id="sidebar", children=[
        dcc.Link(className="click", title=pagina["title"], href=pagina["relative_path"], children=html.Img(
            src=app.get_asset_url(f"icons/icone-{pagina['name']}.svg"), width="35px", height="35px"
            ))
        for pagina in dash.page_registry.values()
        ]),
    html.Div(id="content", children=dash.page_container)
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
