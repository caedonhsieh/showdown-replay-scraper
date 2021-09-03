from urllib.request import Request, urlopen
import json

def load(URL):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as file:
        data = json.loads(file.read().decode())
        return data

def build_url(format='gen8ou'):
    return f'https://pokemonshowdown.com/ladder/{format}.json'

def get_users(data):
    return [user['userid'] for user in data['toplist']]