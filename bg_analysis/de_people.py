import pandas as pd


def get_designers(df):
    designers = df.designers.explode()
    designers = designers.to_frame()
    designers = designers.dropna()
    designers = designers.merge(
        df[
            [
                "id",
                "name",
                "reimplementation",
                "expansion",
                "average",
                "usersrated",
                "yearpublished",
                "wishing",
            ]
        ],
        left_index=True,
        right_index=True,
    )
    return designers


def get_artists(df):
    artists = df.artists.explode()
    artists = artists.dropna()
    artists = artists.to_frame()
    artists = artists.merge(
        df[
            [
                "id",
                "name",
                "reimplementation",
                "expansion",
                "average",
                "usersrated",
                "yearpublished",
                "wishing",
            ]
        ],
        left_index=True,
        right_index=True,
    )
    return artists


def get_publishers(df):
    publishers = df.publishers.explode()
    publishers = publishers.dropna()
    publishers = publishers.to_frame()
    publishers = publishers.merge(
        df[
            [
                "id",
                "name",
                "reimplementation",
                "expansion",
                "average",
                "usersrated",
                "yearpublished",
                "wishing",
            ]
        ],
        left_index=True,
        right_index=True,
    )
    return publishers


def get_categories(df):
    categories = df.categories.explode()
    categories = categories.to_frame()
    categories = categories.dropna()
    categories = categories.merge(
        df[
            [
                "id",
                "name",
                "reimplementation",
                "expansion",
                "average",
                "averageweight",
                "usersrated",
                "wishing",
                "yearpublished",
            ]
        ],
        left_index=True,
        right_index=True,
    )
    categories = categories.sort_values("wishing", ascending=False)
    return categories


def get_mechanics(df):
    mechanics = df.mechanics.explode()
    mechanics = mechanics.to_frame()
    mechanics = mechanics.dropna()
    mechanics = mechanics.merge(
        df[
            [
                "id",
                "name",
                "reimplementation",
                "expansion",
                "average",
                "averageweight",
                "usersrated",
                "wishing",
                "yearpublished",
            ]
        ],
        left_index=True,
        right_index=True,
    )
    mechanics = mechanics.sort_values("wishing", ascending=False)
    return mechanics


def get_families(df):
    families = df.families.explode()
    families = families.to_frame()
    families = families.dropna()
    families = families.merge(
        df[
            [
                "id",
                "name",
                "reimplementation",
                "expansion",
                "average",
                "averageweight",
                "usersrated",
                "wishing",
                "yearpublished",
            ]
        ],
        left_index=True,
        right_index=True,
    )
    families = families.sort_values("wishing", ascending=False)
    return families


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
