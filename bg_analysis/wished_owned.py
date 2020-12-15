import altair as alt
import pandas as pd


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[(df.wishing > 2000) | (df.owned > 13000)]
    #  most_rated = df[df.usersrated > 150]
    #  most_rated = most_rated[most_rated.averageweight != 0]
    #  most_rated = most_rated[most_rated.expansion == False]
    return most_rated


def fig_wished_owned(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                x=alt.X("owned:Q", title="Owned"),
                y=alt.Y("wishing:Q", title="Wishlisted"),
                #  color="yearpublished:O",
                tooltip=["name", "yearpublished", "wishing", "owned", "average", "id"],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Most owned and wished for games", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data
    import altair_saver

    df = get_data()
    fig = fig_wished_owned(df)
    #  fig.show()
    fig.save("charts/wished_owned.html")
    altair_saver.save(fig, "charts/wished_owned.png")
