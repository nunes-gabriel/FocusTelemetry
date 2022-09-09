from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__, title="Dashboard de Teste")

cidades_brasileiras = pd.read_csv(r"\\Server\python-matutino\gabriel.nunes\Documents\GitHub\TCC-GestaoLogistica\testes\cidades.csv")

fig = px.line_mapbox(cidades_brasileiras, lat="lat", lon="lon", color="State", zoom=3, height=300)

app.layout = html.Div([
    html.H1("Dashboard de Teste"),
    dcc.Graph(id="mapa", figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)