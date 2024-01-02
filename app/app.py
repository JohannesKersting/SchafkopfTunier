import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
from flask import Flask
import globals
import os

FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)

server = Flask(__name__)
app = dash.Dash(server=server, title='Schafkopf Tunier', use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME])

def get_tournament_list():
    return [name for name in os.listdir(globals.DATA_DIR) if os.path.isdir(os.path.join(globals.DATA_DIR, name))]

app.layout = html.Div([
    dcc.Store(id='store-tournament_list',
              data=get_tournament_list()),
    dash.page_container
])


@callback(Output('store-tournament_list', 'data', allow_duplicate=True),
          Input('main-tournament-dropdown', 'value'),
          prevent_initial_call=True)
def update_tournament_list_admin(dummy):
    return get_tournament_list()


@callback(Output('store-tournament_list', 'data', allow_duplicate=True),
          Input('add_tournament-alert-created', 'children'),
          prevent_initial_call=True)
def update_tournament_list_main(dummy):
    return get_tournament_list()


if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'True') == "True"
    app.run_server(debug=debug, host='0.0.0.0', port=8050, threaded=True)
