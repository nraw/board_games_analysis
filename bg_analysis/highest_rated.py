import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache
from de import get_data

alt.data_transformers.disable_max_rows()


@lru_cache
def get_data():
    batches = pathlib.Path("data").glob("*.json")
    all_data = {}
    [all_data.update(json.load(open(batch))) for batch in batches]
    df = pd.DataFrame(all_data).T
    df_stats = df.stats.apply(pd.Series)
    df = pd.concat([df, df_stats], axis=1)
    return df


def get_averages(df):
    cut_bins_rating = np.arange(0, 10, 0.5)
    cut_bins_weight = np.arange(0, 5, 0.5)
    ratings = pd.cut(df.average, cut_bins_rating, right=False, labels=False)
    ratings = ratings / 2
    weights = pd.cut(df.averageweight, cut_bins_weight, right=False)
    weights = pd.cut(df.averageweight, cut_bins_weight, right=False, labels=False)
    weights = weights / 2
    return ratings, weights


def rating_dist(ratings, weights):
    rnw = pd.DataFrame(dict(rating=ratings, weight=weights))
    rnw = rnw[(rnw.rating != 0) & (rnw.weight != 0)]
    #  rnw = rnw[~((rnw.rating == 0) & (rnw.weight == 0))]
    rnw = rnw.value_counts()
    rnw = rnw.reset_index()
    rnw = rnw.rename(columns={0: "count"})
    fig = (
        alt.Chart(rnw)
        .mark_rect()
        .encode(
            x="weight:O",
            y=alt.Order("rating:O", sort="descending"),
            color=alt.Color("count:Q", scale=alt.Scale(scheme="blues")),
            tooltip="count",
        )
    ).properties(width=400, height=800)
    fig.show()


def rating_through_time(df):
    fig = (
        alt.Chart(df)
        .mark_point()
        .encode(x="averageweight:Q", y="average:Q", color="color:N")
    ).properties(width=400, height=800)
    fig.show()


def rating_through_time(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 1000]
    #  most_rated = df[df.usersrated > 150]
    most_rated.iloc[0].T
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    most_rated = most_rated[most_rated.yearpublished != 0]
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                y="average:Q",
                x="wishing:Q",
                #  color="yearpublished:O",
                tooltip=["name", "yearpublished", "average"],
                #  size="average",
                opacity="wishing",
            )
        )
        .properties(width=1000, height=400)
        .interactive()
    )
    fig.show()
