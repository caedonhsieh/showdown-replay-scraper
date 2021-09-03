import argparse
import csv
import json
import numpy as np
from pokemon_data import PokemonData

def main():
    args = parse_args()

    pd = PokemonData('pkmn_gen8ou.json')

    with open(args.input_filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = np.empty((0, 2*len(pd)+1), int)
        for row in csv_reader:
            if int(row['time']) < args.min_time or \
                int(row['rating']) < args.min_rating or \
                row['winner'] not in ['0', '1']:
                continue
            all_found = True
            teams = [[], []]
            for team in range(2):
                for pkmn in range(6):
                    key = f'team{team}_pkmn{pkmn}'
                    if key in row:
                        teams[team].append(row[key])
                    else:
                        raise ValueError(f'Invalid csv key: {key}')
            datum = pd.teams_to_datum(teams[0], teams[1], allow_skip=args.allow_skip)
            if datum is None:
                continue
            winner = int(row['winner'])
            loser = (winner-1)*-1

            entry = np.concatenate([datum, np.array([[winner]])], axis=1)
            reverse_entry = np.concatenate([entry[0][len(pd):-1], entry[0][0:len(pd)], np.array([loser])])[None]
            if all_found:
                data = np.concatenate([data, entry, reverse_entry], axis=0)
                
        print(data.shape)
        np.save(args.output_filename, data)
    

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        'input_filename',
        type=str,
        help='Name of file name to read'
    )
    parser.add_argument(
        'output_filename',
        type=str,
        help='Name of file name to write'
    )
    parser.add_argument(
        '--min_rating',
        type=int,
        default=1000,
        help='Filter replays with rating below threshold')
    parser.add_argument(
        '--min_time',
        type=int,
        default=0,
        help="Filter replays with time below threshold"
    )
    parser.add_argument(
        '--allow_skip',
        type=bool,
        default=False,
        help="If false, exclude teams that have pokemon not in the data json; \
            if true, include those teams but skip those pokemon"
    )
    return parser.parse_args()

if __name__ == "__main__":
   main()