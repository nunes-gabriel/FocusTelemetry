from dash import Dash, html, dcc

import dash

app = Dash(
    __name__,
    use_pages=True,
    title="Focus Telemetry",
    update_title="Carregando..."
    )

app.layout = html.Div([
    html.Div(style={"display": "none"}, id="none"),
    html.Ul(id="barra-lateral", children=[
        dcc.Link(title=pagina["title"], href=pagina["relative_path"], children=html.Img(
            src=app.get_asset_url(f"/icons/icone-{pagina['name']}.svg"), width="40px", height="40px"
            ))
        for pagina in dash.page_registry.values()
        ]),
    html.Div(id="conteudo", children=dash.page_container)
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
