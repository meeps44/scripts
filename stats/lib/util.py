import prettyprinter as pp
import pandas as pd
from lib.definitions.classdefinitions import *
import lib.plot as plot
import lib.filter as filter
import lib.compare as scmp
import lib.sqlite_load as sq
import logging
import glob
import re


def get_unique_source_asns(df: pd.DataFrame) -> pd.Series:
    return df["SOURCE_ASN"].unique()


def get_filenames(db_dir:str) -> list:
    ls: list = glob.glob(db_dir)
    return ls


def get_vantage_points(filenames:list) -> list:
    vps = list()
    for file in filenames:
        result = re.search("[a-z]{3}[0-9]", file)
        vps.append(result.group(0))
    return vps


def create_stats(df: pd.DataFrame) -> TracerouteStatistics:
    stats = TracerouteStatistics()
    stats.num_rows_total = get_num_rows(df)
    stats.num_loops = filter.count_loops(df)
    stats.num_cycles = filter.count_cycles(df)
    #stats.num_asns_traversed = get_asns_traversed(df)
    stats.num_fl_changes = len(
        filter.get_rows_with_path_flow_label_changes(df))
    return stats

def get_total_number_of_loops_in_dataset(df: pd.DataFrame):
    return filter.count_loops(df)


def get_num_rows(df: pd.DataFrame) -> int:
    """
    Get number of rows in the dataframe.
    """
    return len(df)


def get_hop_where_path_diverged(df: pd.DataFrame, flowlabel: int, destination_address: str):
    pass


def get_asns_traversed(df: pd.DataFrame) -> list:
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    asns_traversed: list[str] = list()
    for row in df:
        asns_traversed.append(row)


def print_stats(stats: TracerouteStatistics):
    pp.install_extras()
    pp.pprint(stats)


def get_total_number_of_equal_paths(df: pd.DataFrame):
    pass
