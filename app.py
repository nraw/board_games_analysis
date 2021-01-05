from bg_analysis.de import get_data
from bg_analysis.de_people import get_categories
from game_search.get_all_filters import get_all_filters, get_unique_filters
from iterfzf import iterfzf
import pandas as pd
from loguru import logger

import altair as alt

#  import fire
import argh

alt.data_transformers.disable_max_rows()


class App(object):
    """Game Searching App"""

    def __init__(self, df=None):
        self.commands = {
            "Filter": self.filter,
            "Unfilter": self.unfilter,
            "Game": self.get_game,
            "Best": self.get_best,
            "Plot": self.show_plot,
            "Reset": self.reset,
            "Show": self.show,
        }
        self.df = load_data() if df is None else df
        self.reset()
        self.on = True
        #  self.main()

    def reset(self):
        self.df_filtered = self.df
        self.all_filters, self.unique_filters = self._get_filters(self.df)
        self.game = pd.DataFrame()
        self.applied_filters = []

    def main(self):
        self.on = True
        while self.on:
            self._main_phase()

    def _main_phase(self):
        self._get_command()
        if self.command:
            self._execute_command()
        else:
            self.on = False

    def _get_command(self):
        self.command = iterfzf(self.commands.keys())

    def _execute_command(self):
        command_function = self.commands.get(self.command)
        command_function()

    def filter(self):
        self.data_filter = self._get_filter(self.unique_filters)
        if not self.data_filter:
            return None
        self.applied_filters += [self.data_filter]
        self.df_filtered = self._apply_filter(
            self.data_filter, self.df_filtered, self.all_filters
        )
        self.all_filters, self.unique_filters = self._get_filters(self.df_filtered)

    def _get_filter(self, filters):
        data_filter = iterfzf(filters)
        return data_filter

    def unfilter(self):
        self.data_filter = self._get_filter(self.applied_filters)
        if not self.data_filter:
            return None
        self.applied_filters.remove(self.data_filter)
        self.df_filtered = self._apply_filters(self.df)

    def show_plot(self):
        show_plot(self.df_filtered)

    def _get_filters(self, df):
        all_filters = get_all_filters(df)
        unique_filters = get_unique_filters(all_filters)
        return all_filters, unique_filters

    def get_game(self):
        game_name = iterfzf(self.df.sort_values("wishing", ascending=False).name)
        self.game = self.df[self.df.name == game_name]
        self.applied_filters = self._get_game_filters()
        self.df_filtered = self._apply_filters(self.df)

    def _get_game_filters(self):
        applied_filters = list(
            self.all_filters[self.all_filters.id == self.game.id.iloc[0]].property
        )
        return applied_filters

    def _apply_filters(self, df_filtered):
        for data_filter in self.applied_filters:
            df_filtered = self._apply_filter(data_filter, df_filtered, self.all_filters)
        return df_filtered

    def _apply_filter(self, data_filter, df_filtered, all_filters):
        filtered_games = all_filters[all_filters.property == data_filter]
        df_filtered = df_filtered[df_filtered.id.isin(filtered_games.id)]
        return df_filtered

    def get_best(self):
        df_best = []
        for data_filter in self.applied_filters:
            df_best += [
                self._apply_filter(data_filter, self.df, self.all_filters).head(3)
            ]
        self.df_filtered = pd.concat([self.df_filtered] + df_best).drop_duplicates(
            "name"
        )

    def show(self):
        print(self.df_filtered[["name", "average", "averageweight", "wishing"]])
        print("\n".join(self.applied_filters))
        input()


#  df = load_data()
#  self = App(df)


def load_data():
    logger.info("Data loading")
    df = pd.read_json("data/df.json")
    logger.info("Data loaded")
    return df


def show_plot(df_filtered):
    fig = fig_filtered(df_filtered)
    #  fig = fig.properties(title=", ".join(applied_filters))
    fig.show()
    #  fig.save("charts/temp.html")


def fig_filtered(df_filtered, max_limit=1000):
    df_filtered = df_filtered.head(max_limit)
    df_filtered = df_filtered[df_filtered.wishing > 0]
    selection = alt.selection_multi(fields=["recommendations"], bind="legend")
    fig = (
        (
            alt.Chart(df_filtered)
            .mark_point()
            .encode(
                #  x=alt.X(
                #  "averageweight:Q",
                #  title="Weight",
                #  scale=alt.Scale(domain=[0.95, 5], nice=False),
                #  ),
                y=alt.Y("wishing"),
                x=alt.X("average:Q", title="BGG Rating", scale=alt.Scale(zero=False)),
                color=alt.Color("recommendations", title="Recommendations"),
                shape="recommendations",
                opacity=alt.condition(
                    selection,
                    alt.Opacity("wishing:Q", scale=alt.Scale(type="log")),
                    alt.value(0.1),
                ),
                tooltip=[
                    "name",
                    "yearpublished",
                    "recommendations",
                    "wishing",
                    "average",
                    "usersrated",
                    "id",
                ],
            )
        )
        .add_selection(selection)
        .properties(width=800, height=800)
        .interactive()
    )
    return fig


if __name__ == "__main__":
    #  fire.Fire(app_bu)
    #  app = App(df)
    app = App()
    argh.dispatch_commands([app.main])
