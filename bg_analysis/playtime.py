import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    #  most_rated = df[df.wishing > 100]
    #  most_rated = df[df.usersrated > 50]
    most_rated = df
    #  most_rated = most_rated[most_rated.averageweight != 0]
    #  most_rated = most_rated[most_rated.expansion == False]
    #  most_rated = most_rated[most_rated.reimplementation == False]
    return most_rated


def fig_longest_games(df):
    most_rated = get_most_rated(df)
    longest_games = most_rated[most_rated.playingtime > 1000]
    fig = (
        (
            alt.Chart(longest_games)
            .mark_point()
            .encode(
                y=alt.Y(
                    "average:Q",
                    title="BGG Rating",
                    scale=alt.Scale(domain=[-0.1, 10.1], nice=False),
                ),
                x=alt.X(
                    "x:Q",
                    title="Playtime in hours",
                    scale=alt.Scale(type="log", domain=[10, 3000000], nice=False),
                ),
                color=alt.Color("wishing:O", legend=None),
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
        .properties(title="The longest games", width=1000, height=400,)
        .interactive()
    )
    return fig


def fig_longest_games_annotations(df):
    cool_games_list = (
        df.sort_values("playingtime", ascending=False).head(9).name.to_list()
    )
    cool_games_list += ["Europa Universalis"]
    fixes = [("Weltindor's Stones", 0.2)]
    df = fix_annotations(df, fixes, y="average")
    cool_games = df[df.name.isin(cool_games_list)]
    annotation = (
        alt.Chart(cool_games)
        .mark_text(align="left", baseline="middle", fontSize=9, dx=7)
        .encode(y="fix", text="name", x=alt.X("x:Q", scale=alt.Scale(type="log")),)
    ).transform_calculate(x="datum.playingtime / 60")
    return annotation


def fix_annotations(df, fixes, y="wishing"):
    fixes = pd.DataFrame(fixes, columns=["name", "fix"])
    if "fix" in df:
        df = df.drop("fix", axis=1)
    df = df.merge(fixes, on="name", how="left")
    df["fix"] = df.fix.fillna(0) + df[y]
    return df


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig_l = fig_longest_games(df)
    annotation = fig_longest_games_annotations(df)
    (fig_l + annotation).show()
    #  fig_l.save("charts/longest_games.html")
    #  fig_s.save("charts/shortest_games.html")
