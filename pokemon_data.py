import json
import numpy as np

class PokemonData:
    def __init__(self, json_path):
        with open('pkmn_gen8ou.json') as f:
            self.pokemon_list = json.load(f)
        self.pokemon_map = {name: i for i, name in enumerate(self.pokemon_list)}

    def __len__(self):
        return len(self.get_pokemon_list())

    def get_pokemon_list(self):
        return self.pokemon_list
    
    def get_pokemon_map(self):
        return self.pokemon_map

    def team_to_numpy(self, team, allow_skip=False):
        arr = np.zeros((1, len(self)), dtype=int)
        for pokemon_name in team:
            if pokemon_name in self.pokemon_map:
                arr[0][self.pokemon_map[pokemon_name]] = 1
            else:
                if not allow_skip:
                    return None
        return arr

    def teams_to_datum(self, team0, team1, allow_skip=False):
        datum_len = 2*len(self.pokemon_list)
        datum = np.zeros((1, datum_len), dtype=int)
        team0_np = self.team_to_numpy(team0, allow_skip)
        team1_np = self.team_to_numpy(team1, allow_skip)
        if team0_np is None or team1_np is None:
            return None
        datum[0][:len(self)] = team0_np
        datum[0][len(self):] = team1_np
        return datum

    def datum_to_teams(self, datum):
        teams = [[],[]]
        for i in np.nditer(np.where(datum==1)):
            if i < len(self):
                teams[0].append(self.pokemon_list[i])
            else:
                teams[1].append(self.pokemon_list[i%len(self)])
        print(teams)