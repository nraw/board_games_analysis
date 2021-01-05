import altair as alt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

alt.data_transformers.disable_max_rows()


def fig_bga(df):
    bga = df[df.bga]
    fig = (
        alt.Chart(bga)
        .mark_point()
        .encode(
            x=alt.X(
                "averageweight:Q",
                title="Weight",
                #  scale=alt.Scale(domain=[0.95, 5], nice=False),
            ),
            y=alt.Y("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
            color=alt.Color("wishing:O", legend=None),
            tooltip=[
                "name",
                "yearpublished",
                "average",
                "usersrated",
                "id",
                "bestplayer",
            ],
        )
    ).properties(title="Games Available on BGA", width=800, height=400,)
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_bga(df)
    fig.show()
    #  fig.save("charts/rating_weight.html")
    #  fig.save("charts/rating_weight.png")
