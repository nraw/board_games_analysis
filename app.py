from bg_analysis.de import get_data
from bg_analysis.de_people import get_categories
from bg_analysis.get_all_filters import get_all_filters
from iterfzf import iterfzf
import pandas as pd
from loguru import logger

import altair as alt
import fire

alt.data_transformers.disable_max_rows()


def app_td():
    #  df = get_data()
    logger.info("Data loading")
    df = pd.read_json("data/df.json")
    logger.info("Data loaded")
    logger.info("Filters creating")
    all_filters = get_all_filters(df)
    unique_filters = list(all_filters.property.value_counts().index)
    logger.info("Filters created")
    df_filtered, applied_filters = filtering_loop(df, all_filters, unique_filters)
    show_plot(df_filtered, applied_filters)
    return df_filtered, applied_filters


def app_bu():
    #  df = get_data()
    df = pd.read_json("data/df.json")
    game = get_game(df)
    all_filters = get_all_filters(df)
    applied_filters = get_game_filters(game, all_filters)
    df_filtered = apply_data_filters(applied_filters, df, all_filters)
    df_filtered, applied_filters = unfiltering_loop(df, applied_filters, all_filters)
    show_plot(df_filtered, applied_filters)
    return df_filtered, applied_filters


def show_plot(df_filtered, applied_filters):
    fig = fig_filtered(df_filtered)
    fig = fig.properties(title=", ".join(applied_filters))
    fig.save("charts/temp.html")
    fig.show()


def fig_filtered(df_filtered, max_limit=1000):
    df_filtered = df_filtered.head(max_limit)
    fig = (
        (
            alt.Chart(df_filtered)
            .mark_point()
            .encode(
                x=alt.X("averageweight:Q", scale=alt.Scale(zero=False)),
                y=alt.Y("average:Q", scale=alt.Scale(zero=False)),
                color=alt.Color("wishing:Q", scale=alt.Scale(type="log")),
                tooltip=[
                    "name",
                    "yearpublished",
                    "wishing",
                    "average",
                    "usersrated",
                    "id",
                ],
            )
        )
        .properties(title="Rating vs weight", width=800, height=800)
        .interactive()
    )
    return fig


def filtering_loop(df, all_filters, unique_filters):
    df_filtered = df.sort_values("wishing", ascending=False).copy()
    applied_filters = []
    while True:
        data_filter = get_filter(unique_filters)
        if not data_filter:
            break
        df_filtered = apply_filter(data_filter, df_filtered, all_filters)
        applied_filters += [data_filter]
        all_filters = get_all_filters(df_filtered)
        unique_filters = list(all_filters.property.value_counts().index)
        print(df_filtered[["name", "average", "averageweight", "wishing"]])
        print(",  ".join(applied_filters))
        stopper = input("Press enter to add another filter")
        if stopper:
            break
    return df_filtered, applied_filters


def unfiltering_loop(df, applied_filters, all_filters):
    while True:
        data_filter = get_filter(applied_filters)
        if not data_filter:
            break
        applied_filters.remove(data_filter)
        df_filtered = apply_data_filters(applied_filters, df, all_filters)
        print(df_filtered[["name", "average", "averageweight", "wishing"]])
        print(",  ".join(applied_filters))
        stopper = input("Press enter to remove another filter")
        if stopper:
            break
    return df_filtered, applied_filters


def get_filter(unique_filters):
    data_filter = iterfzf(unique_filters)
    return data_filter


def get_game(df):
    game_name = iterfzf(df.sort_values("wishing", ascending=False).name)
    game = df[df.name == game_name]
    return game


def get_game_filters(game, all_filters):
    applied_filters = list(all_filters[all_filters.id == game.id.iloc[0]].property)
    return applied_filters


def apply_data_filters(data_filters, df, all_filters):
    df_filtered = df
    for data_filter in data_filters:
        df_filtered = apply_filter(data_filter, df_filtered, all_filters)
    return df_filtered


def apply_filter(data_filter, df_filtered, all_filters):
    filtered_games = all_filters[all_filters.property == data_filter]
    df_filtered = df_filtered[df_filtered.id.isin(filtered_games.id)]
    return df_filtered


if __name__ == "__main__":
    fire.Fire(app_bu)
