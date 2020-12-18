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


def fig_shortest_games(df):
    most_rated = get_most_rated(df)
    shortest_games = most_rated[most_rated.playingtime <= 20]
    shortest_games = shortest_games[shortest_games.playingtime > 0]
    fig = (
        (
            alt.Chart(shortest_games)
            .mark_point()
            .encode(
                y=alt.Y("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
                x=alt.X(
                    "averageweight:Q",
                    title="Weight",
                    scale=alt.Scale(domain=[0.9, 3.5], nice=False),
                ),
                color=alt.Color("wishing:O", legend=None),
                facet=alt.Facet("x:Q", title="Playing time in minutes"),
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
        .properties(
            title="The shortest games by approximate playing time",
            width=200,
            height=400,
        )
        .interactive()
    )
    return fig


def fig_rating_wished_annotations(df):
    """ sad times, it doesn't allow for annotations on facets """
    cool_games_list = [
        "Happy Salmon",
        "Inhuman Conditions",
        "Zombie Kidz Evolution",
        "Codenames",
        "Hanamikoji",
        "FUSE",
        "5-Minute marvel",
        "KLASK",
        "The Crew: The Quest for Planet Nine",
        "Tic-Tac-Toe",
    ]
    #  fixes = [("Scythe", 300), ("Root", -200), ("Gaia Project", -100)]
    fixes = []
    df = fix_annotations(df, fixes, y="average")
    cool_games = df[df.name.isin(cool_games_list)]
    annotation = (
        alt.Chart(cool_games)
        .mark_text(align="left", baseline="middle", fontSize=9, dx=7)
        .encode(x="averageweight", y="fix", text="name")
    )
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
    #  fig_l = fig_longest_games(df)
    fig_s = fig_shortest_games(df)
    fig_s.show()
    #  fig_l.save("charts/longest_games.html")
    #  fig_s.save("charts/shortest_games.html")
