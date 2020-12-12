import altair as alt
import pandas as pd


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 100]
    #  most_rated = df[df.usersrated > 150]
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    most_rated = most_rated[most_rated.reimplementation == False]
    most_rated = most_rated.dropna(subset=["bestplayers"])
    most_rated = most_rated[~most_rated.bestplayers.str.contains(r"\+")]
    most_rated["bestplayers"] = most_rated.bestplayers.astype("int")
    most_rated = most_rated[most_rated.yearpublished <= 2020]

    return most_rated


def fig_best_players(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                y=alt.Y("average:Q", scale=alt.Scale(zero=False)),
                x=alt.X("averageweight:Q", scale=alt.Scale(type="linear")),
                #  color="yearpublished:O",
                tooltip=[
                    "name",
                    "yearpublished",
                    "average",
                    "averageweight",
                    "wishing",
                    "id",
                ],
                facet=alt.Facet("bestplayers:Q"),
                color="bestplayers:Q",
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(
            title="Games depending on the ideal number of players to play them",
            width=50,
            height=400,
        )
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_best_players(df)
    #  fig.show()
    fig.save("charts/best_players.html")
