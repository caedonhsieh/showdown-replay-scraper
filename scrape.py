import search_scraper as ss
import replay_scraper as rs
import user_scraper as us
import csv
import argparse

def main():
    args = parse_args()

    mode = 'a' if args.append else 'w'
    with open(args.filename, mode=mode) as csv_file:
        fieldnames = [  'time',
                        'rating',
                        'winner',
                        'team0_pkmn0',
                        'team0_pkmn1',
                        'team0_pkmn2',
                        'team0_pkmn3',
                        'team0_pkmn4',
                        'team0_pkmn5',
                        'team1_pkmn0',
                        'team1_pkmn1',
                        'team1_pkmn2',
                        'team1_pkmn3',
                        'team1_pkmn4',
                        'team1_pkmn5']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not args.append:
            writer.writeheader()

        if args.by_top_k_users > 0:
            users = us.get_users(us.load(us.build_url(args.format)))[:args.by_top_k_users]
        else:
            users = [None]
        
        max_page = 25
        for i, user in enumerate(users):
            print(i, user)
            for i in range(args.start, min(args.start+args.num_pages, max_page + 1)):
                replay_json = ss.load(ss.build_url(i, args.format, args.by_rating, user))
                replay_ids = ss.get_replays(replay_json, min_rating = args.min_rating, min_time=args.min_time)
                if len(replay_ids) == 0:
                    break
                for id in replay_ids:
                    try:
                        data = rs.load(rs.build_url(id))
                    except:
                        continue
                    time = rs.get_time(data)
                    rating = rs.get_rating(data)
                    if rating < args.min_rating:
                        continue
                    teams = rs.get_teams(data)
                    if len(teams[0]) != 6 or len(teams[1]) != 6:
                        continue
                    winner_index = rs.get_winner_index(data)
                    writer.writerow({   'time': time,
                                        'rating': rating,
                                        'winner': winner_index,
                                        'team0_pkmn0': teams[0][0],
                                        'team0_pkmn1': teams[0][1],
                                        'team0_pkmn2': teams[0][2],
                                        'team0_pkmn3': teams[0][3],
                                        'team0_pkmn4': teams[0][4],
                                        'team0_pkmn5': teams[0][5],
                                        'team1_pkmn0': teams[1][0],
                                        'team1_pkmn1': teams[1][1],
                                        'team1_pkmn2': teams[1][2],
                                        'team1_pkmn3': teams[1][3],
                                        'team1_pkmn4': teams[1][4],
                                        'team1_pkmn5': teams[1][5]})
            

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        'filename',
        type=str,
        help='Name of file name to write'
    )
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='Page to start scrape')
    parser.add_argument(
        '--num_pages',
        type=int,
        default=1,
        help='Number of pages to scrape')
    parser.add_argument(
        '--format',
        type=str,
        default="gen8ou",
        help='Name of the format name to scrape')
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
        '--append',
        type=bool,
        default=False,
        help="If true, will append data instead of overwrite in filename"
    )
    parser.add_argument(
        '--by_rating',
        type=bool,
        default=False,
        help="If true, will search by highest rating instead of recency"
    )
    parser.add_argument(
        '--by_top_k_users',
        type=int,
        default=0,
        help="Set k, if k>0, will conduct search for each of the top k users"
    )
    return parser.parse_args()

if __name__ == "__main__":
   main()