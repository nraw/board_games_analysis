import altair as alt
import pandas as pd


def get_most_rated(df):
    #  most_rated = df[df.wishing > 10]
    most_rated = df[(df.wanting > 300) | (df.trading > 300)]
    #  most_rated = df[df.usersrated > 150]
    #  most_rated = most_rated[most_rated.averageweight != 0]
    #  most_rated = most_rated[most_rated.expansion == False]
    return most_rated


def fig_want_trade(df):
    most_rated = get_most_rated(df)
    fig = (
        (
            alt.Chart(most_rated)
            .mark_point()
            .encode(
                y=alt.Y("wanting:Q", title="Wanting", scale=alt.Scale()),
                x=alt.X("trading:Q", title="Trading", scale=alt.Scale()),
                color=alt.Color(
                    "average:Q",
                    scale=alt.Scale(scheme="yellowgreenblue"),
                    title="BGG Rating",
                ),
                tooltip=[
                    "name",
                    "yearpublished",
                    "wanting",
                    "trading",
                    "average",
                    "id",
                ],
                #  size="wishing",
                #  opacity="wishing",
            )
        )
        .properties(title="Most traded games", width=1000, height=400)
        .interactive()
    )
    return fig


def fig_want_traded_annotations(df):
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
    fixes = []
    df = fix_annotations(df, fixes, y="wanting")
    cool_games = df[df.name.isin(cool_games_list)]
    annotation = (
        alt.Chart(cool_games)
        .mark_text(align="left", baseline="middle", fontSize=9, dx=7)
        .encode(x="trading", y="fix", text="name")
    )
    return annotation


def fix_annotations(df, fixes, y="wishing"):
    fixes = pd.DataFrame(fixes, columns=["name", "fix"])
    if "fix" in df:
        df = df.drop("fix", axis=1)
    df = df.merge(fixes, on="name", how="left")
    df["fix"] = df.fix.fillna(0) + df[y]
    return df


if __name__ == "__main__":
    from bg_analysis.de import get_data

    df = get_data()
    fig = fig_want_trade(df)
    fig.show()
    #  fig.save("charts/want_trade.html")
    #  fig.save("charts/want_trade.png")
