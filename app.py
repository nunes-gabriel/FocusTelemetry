from dash import Dash, html, dcc, Input, Output

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
    dcc.Location(id="pagina-atual", refresh=False),
    html.Img(id="logo", src=app.get_asset_url("logo.png"), width="120px", height="120px"),
    html.Ul(id="sidebar", children=[
        dcc.Link(className="click", id=f"pgI-{pagina['name']}", title=pagina["title"], href=pagina["relative_path"], children=html.Img(
            src=app.get_asset_url(f"icons/icone-{pagina['name']}.svg"), width="35px", height="35px"
            ))
        for pagina in dash.page_registry.values()
        ]),
    html.Div(id="content", children=dash.page_container)
    ])


@app.callback(
    [Output(f"pgI-{pagina['name']}", "className") for pagina in dash.page_registry.values()],
    Input("pagina-atual", "pathname")
    )
def botao_ativo(path):
    if path in ["/veiculos", "/veiculos/"]:
        return "click", "click-ativo", "click"
    elif path in ["/motoristas", "/motoristas/"]:
        return *["click"] * 2, "click-ativo"
    else:
        return "click-ativo", *["click"] * 2


if __name__ == "__main__":
    app.run_server(debug=False)
