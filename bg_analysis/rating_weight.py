import altair as alt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd


def get_voted(df):
    voted = df[df.usersrated > 100]
    voted = voted[voted.expansion == False]
    voted = voted[voted.reimplementation == False]
    voted = voted[voted.averageweight != 0]
    voted = voted.sort_values("wishing", ascending=False).head(8000)
    return voted


def fig_rating_weight(df):
    voted = get_voted(df)
    base_fig = get_base_fig(voted)
    trendline = get_trendline(voted)
    fig = base_fig + trendline
    return fig


def get_base_fig(voted):
    fig = (
        alt.Chart(voted)
        .mark_point()
        .encode(
            x=alt.X(
                "averageweight:Q",
                title="Weight",
                scale=alt.Scale(domain=[0.95, 5], nice=False),
            ),
            y=alt.Y("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
            opacity="usersrated:O",
            #  color=alt.Color(
            #  "yearpublished:O",
            #  scale=alt.Scale(scheme="yellowgreenblue"),
            #  title="BGG Rating",
            #  ),
            tooltip=[
                "name",
                "yearpublished",
                "average",
                "usersrated",
                "wishing",
                "id",
            ],
        )
    ).properties(title="Rating vs Complexity", width=800, height=800)
    return fig


def get_trendline(voted):
    x, y = linear_regression(voted)
    model_data = pd.DataFrame(dict(x=list(x), y=list(y)))
    fig = (
        alt.Chart(model_data)
        .mark_line()
        .encode(x="x", y="y", color=alt.value("#346176"))
    )
    return fig


def linear_regression(voted):
    model = LinearRegression()
    X = voted.averageweight.to_numpy().reshape(-1, 1)
    model.fit(X, voted.average)
    x = np.arange(1, 6)
    y = model.predict(x.reshape(-1, 1))
    return x, y


def get_correlation(voted):
    correlation = np.corrcoef(voted.average, voted.averageweight)[1, 0]
    return correlation


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_rating_weight(df)
    fig.show()
    #  fig.save("charts/rating_weight.html")
    #  fig.save("charts/rating_weight.png")
