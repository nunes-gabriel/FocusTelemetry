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
    html.Div(className="barra-lateral", children=[
        dcc.Link(title=pagina["title"], href=pagina["path"], children=html.Img(
            src=f"./assets/images/icone-{pagina['name']}.svg", width="40px", height="40px"
            ))
        for pagina in dash.page_registry.values()
        ]),
    html.Div(id="conteudo-pagina", children=dash.page_container)
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
