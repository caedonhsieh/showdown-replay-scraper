from urllib.request import Request, urlopen
import json

def load(URL):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as file:
        data = json.loads(file.read().decode())
        return data

def build_url(id):
    return f'https://replay.pokemonshowdown.com/{id}.json'

def get_teams(replay_data):
    log = replay_data["log"]
    log_lines = log.split('\n')
    
    line_i = next(i for i, line in enumerate(log_lines) if line == '|clearpoke') + 1
    teams = [[], []]
    player_i = 2
    pokemon_i = 3
    while log_lines[line_i].startswith('|poke|'):
        line_elements = log_lines[line_i].split('|')
        team_i = 0 if line_elements[player_i] == 'p1' else 1
        pokemon = line_elements[pokemon_i].split(',')[0]
        teams[team_i].append(pokemon)
        line_i += 1
    return teams

def get_winner_index(replay_data):
    players = [replay_data["p1"], replay_data["p2"]]
    winner = get_winner(replay_data)
    try:
        return players.index(winner)
    except ValueError:
        return -1

def get_winner(replay_data):
    log = replay_data["log"]
    log_lines = log.split('\n')
    winner = ""
    for i in range(len(log_lines)-1, -1, -1):
        if log_lines[i].startswith('|win|'):
            winner = log_lines[i].split('|')[2]
            break
    return winner

def get_rating(replay_data):
    return replay_data["rating"]

def get_time(replay_data):
    return replay_data["uploadtime"]