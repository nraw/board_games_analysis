import altair as alt
from bg_analysis.de_people import get_publishers

alt.data_transformers.disable_max_rows()


def get_aggregates(publishers):
    publishers_agg = publishers[publishers.reimplementation == False]
    publishers_agg = publishers_agg[publishers_agg.expansion == False]
    publishers_agg = publishers_agg.sort_values("usersrated", ascending=False)
    publishers_agg = publishers_agg.groupby("publishers").agg(
        {
            "id": "count",
            "average": "mean",
            "name": lambda x: ", ".join(x[:3]),
            "usersrated": "sum",
            "yearpublished": "max",
        }
    )
    publishers_agg = publishers_agg.reset_index()
    return publishers_agg


def fig_publisher_ratings(df):
    publishers = get_publishers(df)
    publishers_agg = get_aggregates(publishers)
    fig = (
        (
            alt.Chart(publishers_agg)
            .mark_point()
            .encode(
                x=alt.X("id:Q", scale=alt.Scale(zero=True, type="log")),
                y=alt.Y("average:Q", scale=alt.Scale(zero=False)),
                color="yearpublished:O",
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
        .properties(title="publishers ratings vs contributions", width=800, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_publisher_ratings(df)
    fig.show()
    #  fig.save("charts/publishers_ratings.html")
