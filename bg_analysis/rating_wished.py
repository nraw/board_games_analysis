import altair as alt
from altair import datum
import pandas as pd

alt.data_transformers.disable_max_rows()


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 100]
    #  most_rated = df[df.usersrated > 150]
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.expansion == False]
    return most_rated


def fig_rating_wished(df, apply_filter=True):
    if apply_filter:
        most_rated = get_most_rated(df)
    else:
        most_rated = df
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                x=alt.X("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
                y=alt.Y("wishing:Q", title="Wishing", scale=alt.Scale(type="linear")),
                #  color="yearpublished:O",
                tooltip=["name", "yearpublished", "average", "wishing", "id"],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Best board games on BGG", width=1000, height=400)
        .interactive()
    )
    return fig


def fig_rating_wished_annotations(df):
    cool_games_list = [
        "Gloomhaven",
        "Terraforming Mars",
        "Scythe",
        "Pandemic Legacy: Season 1",
        "Brass: Birmingham",
        "Twilight Imperium: Fourth Edition",
        "Spirit Island",
        "Terra Mystica",
        "Root",
        "Nemesis",
        "Too Many Bones",
        "Star Wars: Rebellion",
        "Gaia Project",
        "Kingdom Death: Monster",
    ]
    df = fix_annotations(df)
    cool_games = df[df.name.isin(cool_games_list)]
    annotation = (
        alt.Chart(cool_games)
        .mark_text(align="left", baseline="middle", fontSize=9, dx=7)
        .encode(x="average", y="fix", text="name")
    )
    return annotation


def fix_annotations(df):
    fixes = [("Scythe", 300), ("Root", -200), ("Gaia Project", -100)]
    fixes = pd.DataFrame(fixes, columns=["name", "fix"])
    if "fix" in df:
        df = df.drop("fix", axis=1)
    df = df.merge(fixes, on="name", how="left")
    df["fix"] = df.fix.fillna(0) + df.wishing
    return df


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_rating_wished(df)
    #  fig.show()
    fig.save("charts/rating_wished.html")
    fig.save("charts/rating_wished.png")
