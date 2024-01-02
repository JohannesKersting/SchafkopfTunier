import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback


def get_layout() -> dbc.Container:
    return dbc.Container([
        dbc.Row(dbc.Col(html.H2("Tunier Liste"), width='auto')),
        dbc.Row(dbc.Col(dbc.ListGroup(id='tournament_list-list'))),
    ])


@callback(Output('tournament_list-list', 'children'), Input('store-tournament_list', 'data'))
def update_admin_tournament_list(tournament_list):
    return [dbc.ListGroupItem(tournament) for tournament in tournament_list]
