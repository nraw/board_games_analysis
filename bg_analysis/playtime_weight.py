import altair as alt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

alt.data_transformers.disable_max_rows()


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    #  most_rated = df[df.wishing > 100]
    most_rated = df[df.usersrated > 50]
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    most_rated = most_rated[most_rated.reimplementation == False]
    return most_rated


def fig_playingtime_weight(df):
    most_rated = get_most_rated(df)
    normal_games = most_rated[most_rated.playingtime <= 1440]
    normal_games = normal_games[normal_games.playingtime > 0]
    base_fig = get_base_fig(normal_games)
    trendline = get_trendline(normal_games)
    fig = base_fig + trendline
    return fig


def get_base_fig(normal_games):
    fig = (
        (
            alt.Chart(normal_games)
            .mark_point()
            .encode(
                x=alt.X("playingtime:Q", scale=alt.Scale(type="log", zero=False)),
                y=alt.Y("averageweight:Q", scale=alt.Scale(zero=False)),
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
        .properties(title="Complexity is driven by game length", width=1000, height=400)
        .interactive()
    )
    return fig


def get_trendline(normal_games):
    x, y = linear_regression(normal_games)
    model_data = pd.DataFrame(dict(x=x, y=y))
    fig = (
        alt.Chart(model_data)
        .mark_line()
        .encode(
            y="y",
            x="x",
            #  x=alt.X("x:Q", scale=alt.Scale(type="log")),
            color=alt.value("#346176"),
        )
    )
    return fig


def linear_regression(normal_games):
    model = LinearRegression()
    X = normal_games.playingtime.astype("float").to_numpy().reshape(-1, 1)
    X = np.log(X)
    model.fit(X, normal_games.averageweight)
    x = np.arange(np.log(10), np.log(1200), 1)
    y = model.predict(x.reshape(-1, 1))
    x = np.exp(x)
    return x, y


def get_correlation(normal_games):
    correlation = np.corrcoef(
        normal_games.playingtime.astype("float"), normal_games.averageweight
    )[1, 0]
    return correlation


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    #  fig_l = fig_longest_games(df)
    #  fig_s = fig_shortest_games(df)
    fig_w = fig_playingtime_weight(df)
    fig_w.show()
    fig_w.save("charts/playtime_weight.html")
    #  fig_s.save("charts/shortest_games.html")
