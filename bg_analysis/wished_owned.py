import altair as alt
import pandas as pd


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[(df.wishing > 2000) | (df.owned > 13000)]
    #  most_rated = df[df.usersrated > 150]
    #  most_rated = most_rated[most_rated.averageweight != 0]
    #  most_rated = most_rated[most_rated.expansion == False]
    return most_rated


def fig_wished_owned(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                x=alt.X("owned:Q", title="Owned"),
                y=alt.Y("wishing:Q", title="Wishing"),
                color=alt.Color(
                    "average:Q",
                    scale=alt.Scale(scheme="yellowgreenblue"),
                    title="BGG Rating",
                ),
                tooltip=["name", "yearpublished", "wishing", "owned", "average", "id"],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Most owned and wished for games", width=1000, height=400)
        .interactive()
    )
    return fig


def fig_wished_owned_annotations(df):
    cool_games_list = [
        "Pandemic",
        "Carcassonne",
        "Catan",
        "7 Wonders",
        "Terraforming Mars",
        "Scythe",
        "Gloomhaven",
        "Dominion",
        "Ticket to Ride",
        "Codenames",
        "Love Letter",
        "Munchkin",
        "7 Wonders Duel",
        "Small World",
        "Agricola",
        "Azul",
        "Splendor",
        "King of Tokyo",
        "Scrabble",
        "Risk",
        "Chess",
    ]
    df = fix_annotations(df)
    cool_games = df[df.name.isin(cool_games_list)]
    cool_games = cool_games.sort_values("wishing").drop_duplicates(subset="name")
    annotation = (
        alt.Chart(cool_games)
        .mark_text(align="left", baseline="middle", fontSize=9, dx=7)
        .encode(x="owned", y="fix", text="name")
    )
    return annotation


def fix_annotations(df):
    fixes = [("Scythe", 0), ("Risk", 300), ("7 Wonders Duel", -200)]
    fixes = pd.DataFrame(fixes, columns=["name", "fix"])
    if "fix" in df:
        df = df.drop("fix", axis=1)
    df = df.merge(fixes, on="name", how="left")
    df["fix"] = df.fix.fillna(0) + df.wishing
    return df


if __name__ == "__main__":
    from bg_analysis.de import get_data
    import altair_saver

    df = get_data()
    fig = fig_wished_owned(df)
    fig.show()
    #  fig.save("charts/wished_owned.html")
    #  altair_saver.save(fig, "charts/wished_owned.png")
