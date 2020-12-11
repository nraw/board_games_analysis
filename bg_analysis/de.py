import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache

alt.data_transformers.disable_max_rows()


@lru_cache
def get_data():
    batches = pathlib.Path("data").glob("*.json")
    all_data = {}
    [all_data.update(json.load(open(batch))) for batch in batches]
    df = pd.DataFrame(all_data).T
    df_stats = df.stats.apply(pd.Series)
    df = pd.concat([df, df_stats], axis=1)
    return df
