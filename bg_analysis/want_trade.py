import altair as alt
import pandas as pd


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[(df.wanting > 300) | (df.trading > 300)]
    #  most_rated = df[df.usersrated > 150]
    #  most_rated = most_rated[most_rated.averageweight != 0]
    #  most_rated = most_rated[most_rated.expansion == False]
    return most_rated


def fig_want_trade(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                y=alt.Y("wanting:Q", title="Wanting", scale=alt.Scale()),
                x=alt.X("trading:Q", title="Trading", scale=alt.Scale()),
                color=alt.Color(
                    "average:Q",
                    scale=alt.Scale(scheme="yellowgreenblue"),
                    title="BGG Rating",
                ),
                tooltip=[
                    "name",
                    "yearpublished",
                    "wanting",
                    "trading",
                    "average",
                    "id",
                ],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Most traded games", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_want_trade(df)
    fig.show()
    #  fig.save("charts/want_trade.html")
    #  fig.save("charts/want_trade.png")
