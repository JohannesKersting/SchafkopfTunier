import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
import os

import components.add_tournament as add_tournament
import components.tournament_list as tournament_list
import globals

dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Admin Seite"), width='auto'), style={'marginTop': '10px'}),
    dbc.Row(dbc.Col(tournament_list.get_layout(), width='auto')),
    dbc.Row(dbc.Col(add_tournament.get_layout(), width='auto')),
], fluid=True)
