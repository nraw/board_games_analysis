import altair as alt

from bg_analysis.de_people import get_designers

alt.data_transformers.disable_max_rows()


def get_aggregates(designers):
    designers_agg = designers[designers.reimplementation == False]
    designers_agg = designers_agg[designers_agg.expansion == False]
    designers_agg = designers_agg.sort_values("usersrated", ascending=False)
    designers_agg = designers_agg[designers_agg.designers != "(Uncredited)"]
    designers_agg = designers_agg.groupby("designers").agg(
        {
            "id": "count",
            "average": "mean",
            "name": lambda x: ", ".join(x[:3]),
            "usersrated": "sum",
            "yearpublished": "max",
            "wishing": "sum",
        }
    )
    designers_agg = designers_agg.reset_index()
    designers_agg = designers_agg[designers_agg.usersrated > 100]
    return designers_agg


def fig_designer_ratings(df):
    designers = get_designers(df)
    designers_agg = get_aggregates(designers)
    fig = (
        (
            alt.Chart(designers_agg)
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
                    "designers",
                    "average",
                    "id",
                    "name",
                    "wishing",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Designers ratings vs contributions", width=1000, height=400)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_designer_ratings(df)
    fig.show()
    #  fig.save("charts/designers_ratings.html")
