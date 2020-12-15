import altair as alt
from bg_analysis.de_people import get_publishers
import pandas as pd

alt.data_transformers.disable_max_rows()


def get_aggregates(publishers):
    publishers_agg = publishers.sort_values("usersrated", ascending=False)
    publishers_agg = publishers_agg.groupby("publishers").agg(
        {
            "id": "count",
            "average": "mean",
            "name": lambda x: ", ".join(x[:3]),
            "usersrated": "sum",
            "yearpublished": "max",
            "wishing": "sum",
        }
    )
    publishers_agg = publishers_agg.reset_index()
    top_publishers = publishers_agg.sort_values("id", ascending=False)
    top_threshold = top_publishers.iloc[15].id
    big_publishers = publishers_agg.id > top_threshold
    publishers_agg = publishers_agg[big_publishers]
    return publishers_agg


def fig_publisher_shares(df):
    publishers = get_publishers(df)
    publishers_agg = get_aggregates(publishers)
    fig = (
        (
            alt.Chart(publishers_agg)
            .mark_bar()
            .encode(
                y=alt.Y("publishers:N", sort="-x"),
                x=alt.X("id:Q"),
                color="average:Q",
                tooltip=[
                    "publishers",
                    "average",
                    "id",
                    "name",
                    "usersrated",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Publishers with most games", width=800, height=800)
        .interactive()
    )
    return fig


def get_wishing_aggregates(publishers):
    publishers_agg = publishers.sort_values("wishing", ascending=False)
    publishers_agg = publishers_agg.groupby("publishers").agg(
        {
            "id": "count",
            "average": "mean",
            "name": lambda x: ", ".join(x[:3]),
            "usersrated": "sum",
            "yearpublished": "max",
            "wishing": "sum",
        }
    )
    publishers_agg = publishers_agg.reset_index()
    top_publishers = publishers_agg.sort_values("wishing", ascending=False)
    top_threshold = top_publishers.iloc[15].wishing
    big_publishers = publishers_agg.wishing > top_threshold
    publishers_agg = publishers_agg[big_publishers]
    return publishers_agg


def fig_publisher_wishes(df):
    publishers = get_publishers(df)
    publishers_agg = get_wishing_aggregates(publishers)
    fig = (
        (
            alt.Chart(publishers_agg)
            .mark_bar()
            .encode(
                y=alt.Y("publishers:N", sort="-x"),
                x=alt.X("wishing:Q"),
                color="id:Q",
                tooltip=[
                    "publishers",
                    "average",
                    "id",
                    "name",
                    "usersrated",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Publishers with most wished games", width=800, height=800)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_publisher_shares(publishers)
    #  fig.show()
    #  fig.save("charts/publishers_games.html")
