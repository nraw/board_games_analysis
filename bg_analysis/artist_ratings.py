import altair as alt

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
        }
    )
    artists_agg = artists_agg.reset_index()
    artists_agg = artists_agg[artists_agg.usersrated > 100]
    return artists_agg


def fig_artist_ratings(artists):
    artists_agg = get_aggregates(artists)
    fig = (
        (
            alt.Chart(artists_agg)
            .mark_point()
            .encode(
                x=alt.X("id:Q", scale=alt.Scale(type="log")),
                y=alt.Y("average:Q", scale=alt.Scale(zero=False)),
                color="yearpublished:O",
                tooltip=[
                    "artists",
                    "average",
                    "id",
                    "name",
                    "usersrated",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Artists ratings vs contributions", width=800, height=800)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    #  from bg_analysis.de_people import get_artists

    df = get_data()
    artists = get_artists(df)
    fig = fig_artist_ratings(artists)
    fig.show()
    #  fig.save("charts/artists_ratings.html")
