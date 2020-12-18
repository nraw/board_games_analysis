import altair as alt
import pandas as pd


def fig_rating_year(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 100]
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
                y=alt.Y("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
                x=alt.X("yearpublished:O", title="Year Published"),
                #  color="yearpublished:O",
                color=alt.Color("wishing:O", legend=None),
                tooltip=["name", "yearpublished", "average", "wishing", "id"],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Highest rated games through time", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_rating_year(df)
    fig.show()
    #  fig.save("charts/rating_year.html")
    #  fig.save("charts/rating_year.png")
