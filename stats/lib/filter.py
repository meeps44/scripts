from lib.definitions.classdefinitions import *
from lib.sqlite_load import *
import lib.util as util
from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd
import logging


def find_associated_traces(df: pd.DataFrame) -> list:
    """
    If one row is deemed to be invalid, we also have to remove
    its sibling row.
    """
    associated_rows = list()
    invalid_traces: list = find_invalid_traces(df)
    for row in invalid_traces:
        sibling_indices = find_sibling_indices(row, df)
        associated_rows.append(sibling_indices)
    return associated_rows


def find_sibling_indices(row, df: pd.DataFrame) -> list:
    """
    Returns the indices (row-numbers) of a row's sibling.
    """
    indices = list()
    row_dst_ip = row[1]  # TODO: Find right index
    row_flow_label = row[1]  # TODO: Find right index
    sibling_rows_df: pd.DataFrame = df[(df["DESTINATION_ADDRESS"] == row_dst_ip) & (
        df["SOURCE_FLOW_LABEL"] == row_flow_label)]
    for sibling_row in sibling_rows_df.itertuples():
        if sibling_row != row:
            indices.append(sibling_row.Index)
    return indices


def find_invalid_traces(df: pd.DataFrame):
    """
    Get a list containing the indicies of all rows
    with invalid traces.
    """
    loop_indices: list = util.get_loop_indices(df)
    cycle_indices: list = util.get_cycle_indices(df)
    fl_change_indices: list = util.get_rows_with_path_flow_label_changes(df)
    merged_list = loop_indices + cycle_indices + fl_change_indices
    # Remove duplicate entries
    merged_list = list(dict.fromkeys(merged_list))
    return merged_list


def count_sibling_indices(df: pd.DataFrame) -> int:
    return len(find_invalid_traces(df))


def count_invalid_traces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count traces containing loops, cycles and flow label values
    that changed in-transit.
    """
    loop_indices: list = util.get_loop_indices(df)
    cycle_indices: list = util.get_cycle_indices(df)
    fl_change_indices: list = util.get_rows_with_path_flow_label_changes(df)
    merged_list = loop_indices + cycle_indices + fl_change_indices
    merged_list = list(dict.fromkeys(merged_list))
    return len(merged_list)


def remove_invalid_traces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove traces containing loops, cycles and flow label values
    that changed in-transit.
    """
    loop_indices: list = util.get_loop_indices(df)
    cycle_indices: list = util.get_cycle_indices(df)
    fl_change_indices: list = util.get_rows_with_path_flow_label_changes(df)
    m1 = loop_indices + cycle_indices + fl_change_indices
    sibling_indices: list = find_associated_traces(df)
    merged_list = m1 + sibling_indices
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
