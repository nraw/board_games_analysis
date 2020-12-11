import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache

from loguru import logger
from tqdm import tqdm

alt.data_transformers.disable_max_rows()


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
    df_stats = df.stats.apply(pd.Series)
    df = pd.concat([df, df_stats], axis=1)
    logger.info("Expanded ratings data")
    logger.info("Checking reimplementations")
    df["reimplementation"] = is_reimplementation(df)
    logger.info("Checked reimplementations")
    return df


def is_reimplementation(df):
    reimplementations = df.families.apply(get_game_in_list)
    special_editions = df.name.apply(lambda x: "Edition" in x)
    reimplementations = reimplementations | special_editions
    return reimplementations


def get_game_in_list(families):
    game_in_list = any([family[:5] == "Game:" for family in families])
    return game_in_list


def test_game_in_list():
    families = ["Game: High Frontier", "Space: Pluto"]
    game_in_list = get_game_in_list(families)
    assert game_in_list == True


def get_players_stats(df):
    pass


def restructure_players_stats(players):
    results = pd.DataFrame(players["results"])
    best_ratings = results.loc["best_rating"]
    best_best_ratings = list(best_ratings[best_ratings == best_ratings.max()].index)


def check_plus(best_best_ratings):
    try:
        value = str(round(np.mean(([int(rating) for rating in best_best_ratings]))))
    except ValueError as e:
        value = best_best_ratings[-1]
    return value


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
            },
            "4": {
                "best_rating": 1,
                "recommended_rating": 0,
                "not_recommended_rating": 0,
            },
            "4+": {
                "best_rating": 0,
                "recommended_rating": 0,
                "not_recommended_rating": 1,
            },
        },
    }

