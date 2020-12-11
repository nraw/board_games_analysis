import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache
from bg_analysis.de import get_data

#  from bg_analysis.highest_rated

alt.data_transformers.disable_max_rows()


def plot_rating_year(df):
    from bg_analysis.rating_year import fig_rating_year

    fig = fig_rating_year(df)
    fig.show()


def plot_rating_wished(df):
    from bg_analysis.rating_wished import fig_rating_wished

    fig = fig_rating_wished(df)
    fig.show()


def plot_highest_rated(df):
    pass

