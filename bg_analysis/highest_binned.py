import numpy as np
import pandas as pd
import altair as alt


def get_averages(df):
    cut_bins_rating = np.arange(0, 10, 0.5)
    cut_bins_weight = np.arange(0, 5, 0.5)
    ratings = pd.cut(df.average, cut_bins_rating, right=False, labels=False)
    ratings = ratings / 2
    weights = pd.cut(df.averageweight, cut_bins_weight, right=False)
    weights = pd.cut(df.averageweight, cut_bins_weight, right=False, labels=False)
    weights = weights / 2
    return ratings, weights


def rating_dist(ratings, weights):
    rnw = pd.DataFrame(dict(rating=ratings, weight=weights))
    rnw = rnw[(rnw.rating != 0) & (rnw.weight != 0)]
    #  rnw = rnw[~((rnw.rating == 0) & (rnw.weight == 0))]
    rnw = rnw.value_counts()
    rnw = rnw.reset_index()
    rnw = rnw.rename(columns={0: "count"})
    fig = (
        alt.Chart(rnw)
        .mark_rect()
        .encode(
            x="weight:O",
            y=alt.Order("rating:O", sort="descending"),
            color=alt.Color("count:Q", scale=alt.Scale(scheme="blues")),
            tooltip="count",
        )
    ).properties(width=400, height=800)
    fig.show()

