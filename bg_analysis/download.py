from boardgamegeek import BGGClient
import json
from tqdm import tqdm
from functools import lru_cache

max_game = 350000
batch_size = 500


def get_games(bgg):
    bgg = BGGClient()
    batches = get_batches(max_game, batch_size)
    [get_games_batches(batch, bgg) for batch in tqdm(batches)]


def get_batches(max_game, batch_size):
    a = range(0, max_game, batch_size)
    batches = [x for x in zip(a[:-1], a[1:])]
    return batches


def get_games_batches(batch, bgg):
    games_batch = get_games_batch(batch, bgg)
    games_info = get_games_info(games_batch)
    if len(games_info):
        dump(batch, games_info)
    else:
        print(f"No new data at {batch[0]}")


@lru_cache(1000)
def get_games_batch(batch, bgg):
    games_batch = bgg.game_list(range(*batch))
    return games_batch


def get_games_info(games_batch):
    games_info = {game.id: game._data for game in games_batch if "id" in dir(game)}
    return games_info


def get_game_info(game):
    try:
        game_info = dict(
            name=game.name,
            id=game.id,
            playing_time=game.playing_time,
            min_players=game.min_players,
            max_players=game.max_players,
            rating_average=game.rating_average,
            year=game.year,
        )
    except Exception:
        print("Problem")
    return game_info


def dump(batch, games_info):
    filename = f"data/dump/{batch[0]}-{batch[1]}.json"
    json.dump(games_info, open(filename, "w"))
