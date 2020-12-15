import altair as alt
import pandas as pd

alt.data_transformers.disable_max_rows()


def fig_max_expansions(df):
    expansions = df.sort_values("num_expansions", ascending=False).head(15)
    fig = (
        (
            alt.Chart(expansions)
            .mark_bar()
            .encode(
                y=alt.Y("name:N", sort="-x"),
                x=alt.X("num_expansions:Q"),
                color="average:Q",
                tooltip=[
                    "name",
                    "num_expansions",
                    "average",
                    "id",
                    "usersrated",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Games with most expansions", width=800, height=800)
        .interactive()
    )
    return fig


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 100]
    #  most_rated = df[df.usersrated > 150]
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.average != 0]
    most_rated = most_rated[most_rated.expansion == True]
    return most_rated


def fig_expansions_rating_wished(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                x=alt.X("average:Q", scale=alt.Scale(zero=False)),
                y=alt.Y("wishing:Q", scale=alt.Scale(type="linear")),
                #  color="yearpublished:O",
                tooltip=["name", "yearpublished", "average", "wishing", "id"],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Most wished for expansions", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    #  from bg_analysis.de_people import get_publishers

    df = get_data()
    fig = fig_max_expansions(df)
    fig.show()
    fig_2 = fig_expansions_rating_wished(df)
    fig_2.show()
    fig.save("charts/max_expansions.html")
    fig_2.save("charts/most_wished_expansions.html")
