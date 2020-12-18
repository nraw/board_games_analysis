import altair as alt
import pandas as pd

alt.data_transformers.disable_max_rows()


def get_max_expansions(df):
    expansions = df.sort_values("num_expansions", ascending=False).head(15).copy()

    expansions["trains"] = expansions.categories.apply(lambda x: "Trains" in x)
    expansions["mini"] = expansions.categories.apply(lambda x: "Miniatures" in x)
    expansions["cards"] = expansions.categories.apply(lambda x: "Card Game" in x)
    expansions["type"] = expansions.apply(stupid_rule, axis=1)
    return expansions


def stupid_rule(row):
    if row.trains:
        value = "Trains"
    elif row.mini:
        value = "Miniatures"
    elif row.cards:
        value = "Card Game"
    else:
        value = row["name"]
    return value


def fig_max_expansions(df):
    expansions = get_max_expansions(df)
    fig = (
        (
            alt.Chart(expansions)
            .mark_bar()
            .encode(
                y=alt.Y("name:N", sort="-x", title="Game"),
                x=alt.X("num_expansions:Q", title="Expansions"),
                color=alt.Color("average:Q", title="BGG Rating"),
                tooltip=[
                    "name",
                    "num_expansions",
                    "average",
                    "wishing",
                    "id",
                    "yearpublished",
                ],
            )
        )
        .properties(title="Games with most expansions", width=800, height=400)
        .interactive()
    )
    return fig


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[df.wishing > 100]
    #  most_rated = df[df.usersrated > 150]
    most_rated = most_rated[most_rated.averageweight != 0]
    most_rated = most_rated[most_rated.average != 0]
    most_rated = most_rated[most_rated.expansion == True]
    return most_rated


def fig_expansions_rating_wished(df):
    most_rated = get_most_rated(df)
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
        .properties(title="Most wished for expansions", width=1000, height=400)
        .interactive()
    )
    return fig


def fig_expansions_rating_wished_annotations(df):
    most_rated = get_most_rated(df)
    cool_games_list = (
        most_rated.sort_values("wishing", ascending=False).head(4).name.to_list()
    )
    cool_games_list += ["Spirit Island: Jagged Earth"]
    #  fixes = [("Weltindor's Stones", 0.2)]
    fixes = []
    df = fix_annotations(df, fixes, y="wishing")
    cool_games = df[df.name.isin(cool_games_list)]
    annotation = (
        alt.Chart(cool_games)
        .mark_text(align="left", baseline="middle", fontSize=9, dx=7)
        .encode(y="fix", text="name", x="average")
    )
    return annotation


def fix_annotations(df, fixes=[], y="wishing"):
    fixes = pd.DataFrame(fixes, columns=["name", "fix"])
    if "fix" in df:
        df = df.drop("fix", axis=1)
    df = df.merge(fixes, on="name", how="left")
    df["fix"] = df.fix.fillna(0) + df[y]
    return df


if __name__ == "__main__":
    from bg_analysis.de import get_data

    #  from bg_analysis.de_people import get_publishers

    df = get_data()
    #  fig = fig_max_expansions(df)
    #  fig.show()
    fig_2 = fig_expansions_rating_wished(df)
    fig_2.show()
    #  fig.save("charts/max_expansions.html")
    #  fig_2.save("charts/most_wished_expansions.html")
