from lib.definitions.classdefinitions import *
from lib.sqlite_load import *
from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd
import logging
# logging.basicConfig(level=logging.INFO)


def remove_invalid_traces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove traces containing loops, cycles and flow label values
    that changed in-transit.
    """
    # Remove rows containing loops
    logging.debug("Removing loops")
    df = filter.remove_indices(df, filter.get_loop_indices(df))
    # Remove rows containing cycles
    logging.debug("Removing cycles")
    df = filter.remove_indices(df, filter.get_cycle_indices(df))
    # Remove rows with flow label changes
    logging.debug("Removing rows with flow label changes")
    df = filter.remove_indices(df,
                               filter.get_rows_with_path_flow_label_changes(df))
    return df


def remove_indices(df: pd.DataFrame, indices: list):
    logging.info(
        f"remove_indices: removed {len(indices)} rows from dataset")
    return df.drop(index=indices)
