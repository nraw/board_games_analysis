import altair as alt


def fig_rating_weight(df):
    fig = (
        alt.Chart(df)
        .mark_point()
        .encode(x="averageweight:Q", y="average:Q", color="color:N")
    ).properties(width=400, height=800)
    fig.show()

