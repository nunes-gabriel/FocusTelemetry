from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__, title="Dashboard de Teste")

pontos_entrega = [
    {"id": 1, "local": "Blumenau", "lat": -26.915501, "lon": -49.070904},
    {"id": 1, "local": "Brusque", "lat": -27.097706, "lon": -48.910663},
    {"id": 1, "local": "Tijucas", "lat": -27.235425, "lon": -48.632221},
    {"id": 1, "local": "Florianópolis", "lat": -27.594486, "lon": -48.547696},
    ]

fig = px.line_mapbox(
    pontos_entrega,
    lat="lat",
    lon="lon",
    color="id",
    zoom=3,
    height=500,
    width=500
    )

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=8,
    mapbox_center_lat=-26.915501,
    mapbox_center_lon=-49.070904,
    margin={"r":0,"t":0,"l":0,"b":0}
    )

app.layout = html.Div([
    html.H1("Dashboard de Teste"),
    dcc.Graph(id="mapa", figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
