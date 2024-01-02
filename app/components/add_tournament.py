import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
from classes import Tournament
import os
import globals


def get_layout() -> dbc.Container:
    name_input = html.Div(
        [
            html.P("Tunier Name"),
            dbc.Input(id="add_tournament-name"),
            dbc.FormFeedback(
                type="invalid",
                id="add_tournament-name-feedback"
            ),
        ],
    )

    rounds_input = html.Div(
        [
            html.P("Anzahl der Runden"),
            dbc.Input(type="number", min=1, max=10, step=1, value=2, id="add_tournament-rounds"),
        ],
        id="styled-numeric-input",
    )

    games_per_round_input = html.Div(
        [
            html.P("Anzahl der Spiele pro Runde"),
            dbc.Input(type="number", min=1, max=64, step=1, value=32,
                      id="add_tournament-games_per_round"),
        ],
        id="styled-numeric-input",
    )

    tables_input = html.Div(
        [
            html.P("Tische"),
            dbc.Textarea(rows=5, placeholder="Tisch 1\nTisch 2\n...", id="add_tournament-tables"),
            dbc.FormFeedback(id="add_tournament-tables-feedback", type="invalid"),
        ],
    )

    players_input = html.Div(
        [
            html.P("Spieler"),
            dbc.Textarea(rows=10, placeholder="Spieler 1\nSpieler 2\n...",
                         id="add_tournament-players"),
            dbc.FormFeedback(id="add_tournament-players-feedback", type="invalid"),
        ],
    )

    return dbc.Container([
        html.H2("Neues Tunier erstellen"),
        dbc.Alert(
            id="add_tournament-alert-created",
            dismissable=True,
            is_open=False,
        ),
        dbc.Form([name_input, rounds_input, games_per_round_input, tables_input, players_input, ]),
        dbc.Button("Tunier hinzufügen", id="add_tournament-submit", color="primary"),
    ])


@callback(
    Output("add_tournament-name", "valid"),
    Output("add_tournament-name", "invalid"),
    Output("add_tournament-name-feedback", "children"),
    [Input("add_tournament-name", "value")],
)
def check_name(name):
    if name:
        name = name.strip()

        contains_invalid_chars = any(c in ['/', '\\'] for c in name)
        if contains_invalid_chars:
            return False, True, "Der Name darf keine '/' oder '\\' enthalten."

        exists = os.path.exists(os.path.join(globals.DATA_DIR, name))
        return not exists, exists, "Dieser Name ist bereits vergeben."

    return False, False, ""


@callback(
    Output("add_tournament-tables", "valid"),
    Output("add_tournament-tables", "invalid"),
    Output("add_tournament-tables-feedback", "children"),
    Output("add_tournament-tables-feedback", "type"),
    [Input("add_tournament-tables", "value")],
)
def check_tables(tables):
    if tables:
        tables = tables.strip()
        tables_list = tables.split("\n")
        tables_list = [table.strip() for table in tables_list]

        if len(tables_list) < 1:
            return False, True, "Es muss mindestens ein Tisch angegeben werden.", "invalid"

        # check if all tables are unique
        if len(tables_list) != len(set(tables_list)):
            return False, True, "Keine Tische dürfen doppelt sein.", "invalid"

        # check if all tables are valid
        for table in tables_list:
            if not table:
                return False, True, "Tische dürfen nicht leer sein.", "invalid"
            if any(c in ['/', '\\'] for c in table):
                return False, True, "Tische dürfen keine '/' oder '\\' enthalten.", "invalid"

        return True, False, f"{len(tables_list)} Tische erkannt", "valid"

    return False, False, "", "invalid"


@callback(
    Output("add_tournament-players", "valid"),
    Output("add_tournament-players", "invalid"),
    Output("add_tournament-players-feedback", "children"),
    Output("add_tournament-players-feedback", "type"),
    [Input("add_tournament-players", "value")],
)
def check_players(players):
    if players:
        players = players.strip()
        player_list = players.split("\n")
        player_list = [player.strip() for player in player_list]

        if len(player_list) < 4:
            return False, True, "Es müssem mindestens vier Spieler angegeben werden.", "invalid"

        # check if all tables are unique
        if len(player_list) != len(set(player_list)):
            return False, True, "Keine Spieler dürfen doppelt sein.", "invalid"

        # check if all tables are valid
        for player in player_list:
            if not player:
                return False, True, "Spieler dürfen nicht leer sein.", "invalid"
            if any(c in ['/', '\\'] for c in player):
                return False, True, "Spieler dürfen keine '/' oder '\\' enthalten.", "invalid"

        return True, False, f"{len(player_list)} Spieler erkannt", "valid"

    return False, False, "", "invalid"


@callback(
    Output('add_tournament-alert-created', 'children'),
    Output('add_tournament-alert-created', 'is_open'),
    Output('add_tournament-alert-created', 'color'),
    Input('add_tournament-submit', 'n_clicks'),
    State('add_tournament-name', 'value'),
    State('add_tournament-rounds', 'value'),
    State('add_tournament-games_per_round', 'value'),
    State('add_tournament-tables', 'value'),
    State('add_tournament-players', 'value'),
    State('add_tournament-name', 'valid'),
    State('add_tournament-tables', 'valid'),
    State('add_tournament-players', 'valid'),
    prevent_initial_call=True
)
def create_tournament(n_clicks, name, rounds, games_per_round, tables, players, name_valid, tables_valid, players_valid):
    if n_clicks > 0:

        if not name_valid or not tables_valid or not players_valid or rounds is None or games_per_round is None:
            return "Eingaben sind nicht korrekt oder unvollständig", True, "danger"

        players = players.strip()
        player_list = players.split("\n")
        player_list = [player.strip() for player in player_list]

        tables = tables.strip()
        tables_list = tables.split("\n")
        tables_list = [table.strip() for table in tables_list]

        tournament = Tournament(name.strip(), rounds, games_per_round, tables_list, player_list)
        return f"Neues Tunier: {tournament}", True, "success"
