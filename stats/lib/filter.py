from lib.definitions.classdefinitions import *
from lib.sqlite_load import *
import lib.util as util
from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd
import logging


def remove_invalid_traces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove traces containing loops, cycles and flow label values
    that changed in-transit.
    """
    loop_indices: list = util.get_loop_indices(df)
    cycle_indices: list = util.get_loop_indices(df)
    fl_change_indices: list = util.get_rows_with_path_flow_label_changes(df)
    # Remove rows containing loops
    logging.critical("Removing loops")
    df = remove_indices(df, loop_indices)
    # Remove rows containing cycles
    logging.critical("Removing cycles")
    df = remove_indices(df, cycle_indices)
    # Remove rows with flow label changes
    logging.critical("Removing rows with flow label changes")
    df = remove_indices(df, fl_change_indices)
    return df


def remove_indices(df: pd.DataFrame, indices: list):
    logging.critical(
        f"remove_indices: removed {len(indices)} rows from dataset")
    return df.drop(index=indices)
