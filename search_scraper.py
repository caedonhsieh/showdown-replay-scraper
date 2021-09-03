from urllib.request import Request, urlopen
import json

def load(URL):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as file:
        data = json.loads(file.read().decode())
        return data

def build_url(page=1, format='gen8ou', by_rating=False, user=None):
    url = f'https://replay.pokemonshowdown.com/search.json?format={format}&page={page}'
    if user is not None:
        url = ''.join([url, f'&user={user}'])
    elif by_rating:
        url = ''.join([url, '&rating'])
    return url

def get_replays(data, min_rating = 1000, min_time = 0):
    ids = []
    for replay in data:
        if 'rating' in replay and replay['rating'] < min_rating:
            continue
        if replay['uploadtime'] < min_time:
            continue
        ids.append(replay['id'])
    return ids
