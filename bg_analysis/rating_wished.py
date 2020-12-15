import altair as alt
import pandas as pd


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 100]
    #  most_rated = df[df.usersrated > 150]
    most_rated.iloc[0].T
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    return most_rated


def fig_rating_wished(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                x=alt.X("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
                y=alt.Y("wishing:Q", title="Wished", scale=alt.Scale(type="linear")),
                #  color="yearpublished:O",
                tooltip=["name", "yearpublished", "average", "wishing", "id"],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Best games on BGG", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_rating_wished(df)
    #  fig.show()
    fig.save("charts/rating_wished.html")
    fig.save("charts/rating_wished.png")
