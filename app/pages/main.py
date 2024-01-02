import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_qr_manager as dqm
import socket
import os

dash.register_page(__name__)

layout = dbc.Container([
    dqm.DashQrGenerator(
        id='qr-code',
        data=f'http://{socket.gethostbyname(socket.gethostname())}:8050/main',
        framed=True,
    ),
    dbc.Row(dbc.Col(dcc.Dropdown(id='main-tournament-dropdown', persistence=True, persistence_type='session'))),
    dbc.Row(dbc.Col(html.H1("Hauptseite"), width='auto'), style={'marginTop': '10px'}),
], fluid=True)

@callback(
    Output('main-tournament-dropdown', 'options'),
    Input('store-tournament_list', 'data')
)
def update_tournament_dropdown(tournament_list):
    return tournament_list
