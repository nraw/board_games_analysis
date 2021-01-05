import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache
from bg_analysis.de import get_data
from loguru import logger

from bg_analysis.rating_wished import fig_rating_wished, fig_rating_wished_annotations
from bg_analysis.rating_year import fig_rating_year
from bg_analysis.wished_owned import fig_wished_owned, fig_wished_owned_annotations
from bg_analysis.rating_weight import fig_rating_weight
from bg_analysis.players import fig_best_players
from bg_analysis.playtime import fig_longest_games, fig_longest_games_annotations
from bg_analysis.shortest_games import fig_shortest_games
from bg_analysis.playtime_weight import fig_playingtime_weight
from bg_analysis.artist_ratings import fig_artist_ratings
from bg_analysis.designer_ratings import fig_designer_ratings
from bg_analysis.publisher_ratings import fig_publisher_ratings
from bg_analysis.publisher_shares import fig_publisher_shares, fig_publisher_wishes
from bg_analysis.categories import fig_best_categories
from bg_analysis.mechanics import fig_best_mechanics
from bg_analysis.expansions import (
    fig_max_expansions,
    fig_expansions_rating_wished,
    fig_expansions_rating_wished_annotations,
)
from bg_analysis.want_trade import fig_want_trade, fig_want_traded_annotations
from bg_analysis.susd import fig_susd_dt
from bg_analysis.bga import fig_bga

alt.data_transformers.disable_max_rows()


def generate_all_charts():
    df = get_data()
    save_chart(fig_rating_wished, df, "rating_wished", fig_rating_wished_annotations)
    save_chart(fig_wished_owned, df, "wished_owned", fig_wished_owned_annotations)
    save_chart(fig_want_trade, df, "want_trade", fig_want_traded_annotations)
    save_chart(fig_rating_weight, df, "rating_weight")
    save_chart(fig_best_players, df, "best_players")
    save_chart(fig_shortest_games, df, "shortest_games")
    save_chart(fig_longest_games, df, "longest_games", fig_longest_games_annotations)
    save_chart(fig_playingtime_weight, df, "playingtime_weight")  # problem
    save_chart(fig_artist_ratings, df, "artists_ratings")
    save_chart(fig_designer_ratings, df, "designers_ratings")
    #  save_chart(fig_publisher_ratings, df, "publishers_ratings")
    save_chart(fig_publisher_shares, df, "publishers_shares")
    save_chart(fig_publisher_wishes, df, "publishers_wishes")
    save_chart(fig_best_categories, df, "categories")
    save_chart(fig_best_mechanics, df, "mechanics")
    save_chart(fig_max_expansions, df, "max_expansions")
    save_chart(
        fig_expansions_rating_wished,
        df,
        "most_wished_expansions",
        fig_expansions_rating_wished_annotations,
    )
    save_chart(fig_rating_year, df, "rating_year")
    save_chart(fig_susd_dt, df, "susd_dt")
    save_chart(fig_bga, df, "bga")


def save_chart(f, df, chart_name, annotation_f=None):
    logger.info(f"Generating chart {chart_name}")
    fig = f(df)
    html_chart = f"charts/{chart_name}.html"
    png_chart = f"charts/{chart_name}.png"
    fig.save(html_chart)
    if annotation_f:
        fig += annotation_f(df)
    fig.save(png_chart)
    logger.info(f"Charts {html_chart} and {png_chart} saved")


def open_chart(f, df):
    fig = f(df)
    fig.show()
