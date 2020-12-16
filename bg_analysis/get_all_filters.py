from bg_analysis.rating_wished import fig_rating_wished
from bg_analysis.de import get_data
from bg_analysis.de_people import get_categories, get_mechanics, get_families
from iterfzf import iterfzf
import pandas as pd


def get_all_filters(df):
    categories_filter = get_categories_filter(df)
    mechanics_filter = get_mechanics_filter(df)
    best_players_filter = get_best_players_filter(df)
    families_filter = get_families_filter(df)
    all_filters = pd.concat(
        [categories_filter, mechanics_filter, best_players_filter, families_filter]
    )
    return all_filters


def get_categories_filter(df):
    categories = get_categories(df)
    categories["property"] = categories.categories.apply(lambda x: "Category: " + x)
    categories_filter = categories[["id", "property"]]
    return categories_filter


def get_mechanics_filter(df):
    mechanics = get_mechanics(df)
    mechanics["property"] = mechanics.mechanics.apply(lambda x: "Mechanic: " + x)
    mechanics_filter = mechanics[["id", "property"]]
    return mechanics_filter


def get_best_players_filter(df):
    filtered_df = df.dropna(subset=["bestplayers"])
    best_players_filter = filtered_df[~filtered_df.bestplayers.str.contains(r"\+")][
        ["id"]
    ].copy()
    best_players_filter["property"] = df["bestplayers"].apply(
        lambda x: "Best Players: " + x if x else None
    )
    best_players_filter = best_players_filter.dropna()
    return best_players_filter


def get_families_filter(df):
    families = get_families(df)
    families_filter = families[["families", "id",]].rename(
        columns={"families": "property"}
    )
    return families_filter
