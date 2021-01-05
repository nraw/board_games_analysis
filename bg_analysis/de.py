import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache

from loguru import logger
from tqdm import tqdm
from bg_analysis.de_geeklist import get_geeklist

tqdm.pandas()


@lru_cache(1)
def get_data():
    logger.info("Loading jsons.")
    batches = pathlib.Path("data/dump").glob("*.json")
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
    df["game_family"] = get_game_family_names(df)
    df["reimplementation"] = is_reimplementation(df)
    logger.info("Checked reimplementations")
    logger.info("Obtaining best players")
    df["bestplayers"] = get_players_stats(df)
    logger.info("Obtained best players")
    logger.info("Obtaining number of expansions")
    df["num_expansions"] = df.expansions.apply(len)
    logger.info("Obtained number of expansions")
    logger.info("Obtaining Dice Tower geeklist")
    dice_tower = get_geeklist("265480")
    df["dice_tower_excellence"] = df.id.isin(dice_tower)
    logger.info("Obtained Dice Tower geeklist")
    logger.info("Obtaining SUSD geeklist")
    susd = get_geeklist("244099")
    df["susd"] = df.id.isin(susd)
    logger.info("Obtained SUSD geeklist")
    logger.info("Obtaining BGA geeklist")
    bga = get_geeklist("252354")
    df["bga"] = df.id.isin(bga)
    logger.info("Obtained BGA geeklist")
    return df


def get_game_family_names(df):
    game_families = df.families.apply(get_game_in_list)
    return game_families


def is_reimplementation(df):
    max_game_family_rated = (
        df[df.game_family != ""].groupby("game_family")["usersrated"].max()
    )
    max_max = df.game_family.apply(lambda x: max_game_family_rated.get(x))
    is_main_game = df.usersrated == max_max
    special_editions = df.name.apply(lambda x: "Edition" in x)
    reimplementations = (
        (df.game_family != "") & (is_main_game != True)
    ) | special_editions
    return reimplementations


def get_game_in_list(families):
    game_in_list = [family for family in families if family[:5] == "Game:"]
    if game_in_list:
        game = game_in_list[0].replace("Game: ", "")
    else:
        game = ""
    return game


def get_players_stats(df):
    bestplayers = df.suggested_players.progress_apply(restructure_players_stats)
    return bestplayers


def restructure_players_stats(players):
    if players:
        results = pd.DataFrame(players["results"])
        best_ratings = results.loc["best_rating"]
        best_best_ratings = list(best_ratings[best_ratings == best_ratings.max()].index)
        bestplayer = get_best_num_players(best_best_ratings)
    else:
        bestplayer = None
    return bestplayer


def get_best_num_players(best_best_ratings):
    try:
        bestplayers = str(
            round(np.mean(([int(rating) for rating in best_best_ratings])))
        )
    except ValueError:
        bestplayers = best_best_ratings[-1]
    return bestplayers


def test_game_in_list():
    families = ["Game: High Frontier", "Space: Pluto"]
    game_in_list = get_game_in_list(families)
    assert game_in_list
