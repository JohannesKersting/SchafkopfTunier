import os
import json
import globals

class Tournament:
    def __init__(self, name, rounds, games_per_round, tables, players, ):

        self.config = {
            'name': name,
            'rounds': rounds,
            'games_per_round': games_per_round,
            'total_games': rounds * games_per_round,
            'tables': tables,
            'players': players,

        }
        self.path = os.path.join(globals.DATA_DIR, name)

        os.mkdir(self.path)
        save_file = open(os.path.join(self.path, "config.json"), "w")
        json.dump(self.config, save_file)
        save_file.close()

    def __repr__(self):
        return (f"{self.config['name']}: {self.config['rounds']} Runden mit "
                f"{self.config['games_per_round']} Spielen pro Runde an {len(self.config['tables'])} Tischen mit "
                f"{len(self.config['players'])} Spielern.")

