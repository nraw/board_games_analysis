import altair as alt

from bg_analysis.de_people import get_artists

alt.data_transformers.disable_max_rows()


def get_aggregates(artists):
    artists_agg = artists[artists.reimplementation == False]
    artists_agg = artists_agg[artists_agg.expansion == False]
    artists_agg = artists_agg.sort_values("usersrated", ascending=False)
    artists_agg = artists_agg[artists_agg.artists != "(Uncredited)"]
    artists_agg = artists_agg.groupby("artists").agg(
        {
            "id": "count",
            "average": "mean",
            "name": lambda x: ", ".join(x[:3]),
            "usersrated": "sum",
            "yearpublished": "max",
            "wishing": "sum",
        }
    )
    artists_agg = artists_agg.reset_index()
    artists_agg = artists_agg[artists_agg.usersrated > 100]
    return artists_agg


def fig_artist_ratings(df):
    artists = get_artists(df)
    artists_agg = get_aggregates(artists)
    fig = (
        (
            alt.Chart(artists_agg)
            .mark_point()
            .encode(
                x=alt.X(
                    "id:Q",
                    title="Contributions",
                    scale=alt.Scale(type="log", nice=False, domain=[0.9, 500]),
                ),
                y=alt.Y(
                    "average:Q", title="Average BGG Rating", scale=alt.Scale(zero=False)
                ),
                color=alt.Color("wishing:O", legend=None),
                tooltip=[
                    "artists",
                    "average",
                    "id",
                    "name",
                    "wishing",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Artists ratings vs contributions", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_artist_ratings(df)
    fig.show()
    #  fig.save("charts/artists_ratings.html")
