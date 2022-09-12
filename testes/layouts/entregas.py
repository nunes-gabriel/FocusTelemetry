from dash import html, dcc
import plotly.express as px


def entregas_lista() -> html.Div:
    return html.Div(
        className="pagina-entregas-lista",
        children=[
            dcc.Input(
                className="barra-pesquisa",
                placeholder="Digite um código de entrega para pesquisar...",
                id="entregas-pesquisa"
                ),
            html.Div(
                className="lista-entregas",
                id="entregas-lista"
                )
            ]
        )


def entregas_analise(id: int) -> html.Div:
    return html.Div(
        className="pagina-entregas-analise",
        children=[
            html.Div(
                className="box-mapa-rotas",
                children=[
                    html.H2("Rotas de Entrega"),
                    dcc.Graph(
                        className="mapa-entregas",
                        id="mapa-entregas"
                        )
                    ]
                ),
            html.Div(
                className="box-informacoes",
                id="box-informacoes",
                children="Nenhuma entrega foi selecionada"
                )
            ]
        )
