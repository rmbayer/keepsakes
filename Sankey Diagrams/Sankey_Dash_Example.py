import json
import urllib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import webbrowser

url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
response = urllib.request.urlopen(url)
data = json.loads(response.read())

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.P("Opacity"),
    dcc.Slider(id='opacity', min=0, max=1, 
               value=0.5, step=0.1)
])

@app.callback(
    Output("graph", "figure"), 
    [Input("opacity", "value")])
def display_sankey(opacity):
    opacity = str(opacity)

    # override gray link colors with 'source' colors
    node = data['data'][0]['node']
    link = data['data'][0]['link']

    # Change opacity
    node['color'] = [
        'rgba(255,0,255,{})'.format(opacity) 
        if c == "magenta" else c.replace('0.8', opacity) 
        for c in node['color']]

    link['color'] = [
        node['color'][src] for src in link['source']]

    fig = go.Figure(go.Sankey(link=link, node=node))
    fig.update_layout(font_size=10)

    return fig

webbrowser.open_new("http://localhost:8050")
app.run_server(use_reloader=False)