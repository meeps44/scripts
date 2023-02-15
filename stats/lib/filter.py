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
    cycle_indices: list = util.get_cycle_indices(df)
    fl_change_indices: list = util.get_rows_with_path_flow_label_changes(df)
    merged_list = loop_indices + cycle_indices + fl_change_indices
    # Remove duplicate entries
    merged_list = list(dict.fromkeys(merged_list))
    # Remove rows with invalid entries
    logging.critical("Removing rows with invalid traces")
    df = remove_indices(df, merged_list)
    return df


def remove_indices(df: pd.DataFrame, indices: list):
    logging.critical(
        f"remove_indices: removed {len(indices)} rows from dataset")
    return df.drop(index=indices)
