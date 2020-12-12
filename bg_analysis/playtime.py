import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    #  most_rated = df[df.wishing > 100]
    most_rated = df[df.usersrated > 50]
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    most_rated = most_rated[most_rated.reimplementation == False]
    return most_rated


def fig_longest_games(df):
    most_rated = get_most_rated(df)
    longest_games = most_rated[most_rated.playingtime > 1000]
    fig = (
        (
            alt.Chart(longest_games)
            .mark_point()
            .encode(
                y=alt.Y("average:Q", scale=alt.Scale(zero=False)),
                x=alt.X("x:Q", scale=alt.Scale(type="log")),
                #  color="yearpublished:O",
                tooltip=[
                    "name",
                    "yearpublished",
                    "playingtime",
                    "average",
                    "averageweight",
                    "wishing",
                    "usersrated",
                    "id",
                ],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .transform_calculate(x="datum.playingtime / 60")
        .properties(title="The longest games in hours", width=1000, height=400)
        .interactive()
    )
    return fig


def fig_shortest_games(df):
    most_rated = get_most_rated(df)
    shortest_games = most_rated[most_rated.playingtime <= 20]
    shortest_games = shortest_games[shortest_games.playingtime > 0]
    fig = (
        (
            alt.Chart(shortest_games)
            .mark_point()
            .encode(
                y=alt.Y("average:Q", scale=alt.Scale(zero=False)),
                x=alt.X("averageweight:O", scale=alt.Scale(type="linear")),
                #  color="yearpublished:O",
                facet=alt.Facet("x:Q"),
                tooltip=[
                    "name",
                    "yearpublished",
                    "playingtime",
                    "average",
                    "averageweight",
                    "wishing",
                    "usersrated",
                    "id",
                ],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .transform_calculate(x="round(datum.playingtime / 5)*5")
        .properties(title="The shortest games in minutes", width=200, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    #  fig_l = fig_longest_games(df)
    #  fig_s = fig_shortest_games(df)
    #  fig_l.save("charts/longest_games.html")
    #  fig_s.save("charts/shortest_games.html")
