import altair as alt
import pandas as pd

from bg_analysis.de_people import get_mechanics

alt.data_transformers.disable_max_rows()


def get_most_rated(mechanics):
    #  most_rated = df[df.wishing > 10]
    #  most_rated = mechanics[mechanics.wishing > 100]
    most_rated = mechanics[mechanics.usersrated > 150]
    #  most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    #  most_rated = most_rated[most_rated.reimplementation == False]
    most_rated = most_rated[most_rated.yearpublished <= 2020]

    return most_rated


def fig_best_mechanics(df):
    mechanics = get_mechanics(df)
    most_rated = get_most_rated(mechanics)
    fig = (
        alt.Chart(most_rated)
        .mark_point()
        .encode(
            y=alt.Y("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
            x=alt.X("averageweight:Q", title="Weight", scale=alt.Scale(type="linear")),
            #  color="yearpublished:O",
            tooltip=[
                "name",
                "yearpublished",
                "average",
                "averageweight",
                "wishing",
                "id",
            ],
            facet=alt.Facet(
                "mechanics:N",
                columns=5,
                sort=alt.EncodingSortField("name", op="count", order="descending"),
            ),
            color=alt.Color("wishing:O", legend=None),
            #  size="wishing",
            #  opacity="wishing",
        )
    ).properties(title="Board Game by Mechanics", width=100, height=100,)
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_best_mechanics(df)
    fig.show()
    #  fig.save("charts/mechanics.html")
