import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache

from loguru import logger
from tqdm import tqdm

alt.data_transformers.disable_max_rows()

tqdm.pandas()

@lru_cache(1)
def get_data():
    logger.info("Loading jsons.")
    batches = pathlib.Path("data").glob("*.json")
    all_data = {}
    _ = [all_data.update(json.load(open(batch))) for batch in tqdm(batches)]
    logger.info("Loaded jsons.")
    logger.info("Generating dataframe")
    df = pd.DataFrame(all_data).T
    logger.info("Expanding ratings data")
    df_stats = df.stats.progress_apply(pd.Series)
    df = pd.concat([df, df_stats], axis=1)
    logger.info("Expanded ratings data")
    logger.info("Checking reimplementations")
    df["reimplementation"] = is_reimplementation(df)
    logger.info("Checked reimplementations")
    logger.info("Obtaining best players")
    df['bestplayers'] = restructure_players_stats(df.players)
    logger.info("Obtained best players")
    return df


def is_reimplementation(df):
    reimplementations = df.families.apply(get_game_in_list)
    special_editions = df.name.apply(lambda x: "Edition" in x)
    reimplementations = reimplementations | special_editions
    return reimplementations


def get_game_in_list(families):
    game_in_list = any([family[:5] == "Game:" for family in families])
    return game_in_list


def get_players_stats(df):
    bestplayers = df.suggested_players.progress_apply(restructure_players_stats)


def restructure_players_stats(players):
    if players:
        results = pd.DataFrame(players["results"])
        best_ratings = results.loc["best_rating"]
        best_best_ratings = list(best_ratings[best_ratings == best_ratings.max()].index)
        bestplayers = get_best_num_players(best_best_ratings)
    else:
        bestplayers = None
    return bestplayers



def get_best_num_players(best_best_ratings):
    try:
        bestplayers = str(round(np.mean(([int(rating) for rating in best_best_ratings]))))
    except ValueError as e:
        bestplayers = best_best_ratings[-1]
    return bestplayers


def test_game_in_list():
    families = ["Game: High Frontier", "Space: Pluto"]
    game_in_list = get_game_in_list(families)
    assert game_in_list == True



def test_restructure():
    players = {
        "total_votes": 1,
        "results": {
            "1": {
                "best_rating": 0,
                "recommended_rating": 0,
                "not_recommended_rating": 1,
            },
            "2": {
                "best_rating": 1,
                "recommended_rating": 0,
                "not_recommended_rating": 0,
            },
            "3": {
                "best_rating": 1,
                "recommended_rating": 0,
                "not_recommended_rating": 0,
            "3+": {
                "best_rating": 0,
                "recommended_rating": 0,
                "not_recommended_rating": 1,
            },
        },
    }

