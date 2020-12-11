import json
import altair as alt
import pandas as pd
import pathlib
import numpy as np
from functools import lru_cache

from loguru import logger
from tqdm import tqdm

alt.data_transformers.disable_max_rows()


@lru_cache(1)
def get_data():
    logger.info("Loading jsons.")
    batches = pathlib.Path("data").glob("*.json")
    all_data = {}
    _ = [all_data.update(json.load(open(batch))) for batch in tqdm(batches)]
    logger.info("Loaded jsons.")
    logger.info("Generating dataframe")
    df = pd.DataFrame(all_data).T
    logger.info("Expanding ratings data")
    df_stats = df.stats.apply(pd.Series)
    df = pd.concat([df, df_stats], axis=1)
    logger.info("Expanded ratings data")
    return df
