import altair as alt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

alt.data_transformers.disable_max_rows()


def get_voted(df):
    voted = df  # [df.usersrated > 100]
    #  voted = voted[voted.expansion == False]
    #  voted = voted[voted.reimplementation == False]
    voted = voted[voted.averageweight != 0]
    voted = voted[voted["recommendations"] != "Other"]
    return voted


def susd_dice(df):
    df["recommendations"] = df.susd + 2 * df.dice_tower_excellence
    mapping = {0: "Other", 1: "SUSD", 2: "DT", 3: "SUSD & DT"}
    df["recommendations"] = df.recommendations.apply(lambda x: mapping[x])
    return df


def fig_susd_dt(df, apply_filter=True):
    df = susd_dice(df)
    if apply_filter:
        voted = get_voted(df)
    else:
        voted = df
    fig = get_base_fig(voted)
    return fig


def get_base_fig(voted):
    selection = alt.selection_multi(fields=["recommendations"], bind="legend")
    fig = (
        (
            alt.Chart(voted)
            .mark_point()
            .encode(
                x=alt.X(
                    "averageweight:Q",
                    title="Weight",
                    scale=alt.Scale(domain=[0.95, 5], nice=False),
                ),
                y=alt.Y("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
                color="recommendations:N",
                opacity=alt.condition(
                    selection,
                    alt.Opacity("wishing:Q", scale=alt.Scale(type="log"), legend=None),
                    alt.value(0.1),
                ),
                tooltip=[
                    "name",
                    "yearpublished",
                    "recommendations",
                    "average",
                    "usersrated",
                    "id",
                ],
            )
        )
        .properties(
            title="Dice Tower Certificate of Excellence and Shut up & Sit Down Recommendations",
            width=800,
            height=400,
        )
        .add_selection(selection)
    )
    return fig


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_susd_dt(df)
    fig.show()
    #  fig.save("charts/rating_weight.html")
    #  fig.save("charts/rating_weight.png")
