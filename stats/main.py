from os.path import expanduser
import matplotlib.pyplot as plt
from lib.definitions.classdefinitions import *
import lib.plot as plot
import lib.filter as filter
import lib.compare as scmp
import lib.sqlite_load as sq
import prettyprinter as pp
import pandas as pd
import logging
import glob
import re

def print_source_asns(df: pd.DataFrame):
    src_asns = df["SOURCE_ASN"].unique()
    print(src_asns)


def get_total_number_of_unique_destination_asns(df: pd.DataFrame):
    pass


def get_num_rows(df: pd.DataFrame) -> int:
    """
    Get number of rows in the dataframe.
    """
    return len(df)


def get_total_number_of_loops_in_dataset(df: pd.DataFrame):
    return filter.count_loops(df)


def get_percentage_of_time_path_was_equal(df: pd.DataFrame, vp: VantagePoint):
    if vp.ams3:
        pass
    elif vp.blr1:
        pass
    elif vp.fra1:
        pass
    elif vp.lon1:
        pass
    elif vp.nyc1:
        pass
    elif vp.sfo3:
        pass
    elif vp.sgp1:
        pass
    elif vp.tor1:
        pass


def get_total_percentage_of_time_path_was_equal(df: pd.DataFrame):
    pass


def print_stats(stats: TracerouteStatistics):
    pp.install_extras()
    pp.pprint(stats)


def create_stats(df: pd.DataFrame) -> TracerouteStatistics:
    stats = TracerouteStatistics()
    stats.num_rows_total = get_num_rows(df)
    stats.num_loops = filter.count_loops(df)
    stats.num_cycles = filter.count_cycles(df)
    #stats.num_asns_traversed = get_asns_traversed(df)
    stats.num_fl_changes = len(
        filter.get_rows_with_path_flow_label_changes(df))
    return stats


def get_filenames(db_dir:str) -> list:
    ls: list = glob.glob(db_dir)
    return ls


def get_vantage_points(filenames:list) -> list:
    vps = list()
    for file in filenames:
        result = re.search("[a-z]{3}[0-9]", file)
        vps.append(result.group(0))
    return vps


def main():
    source_flow_labels = [0, 255, 65280, 983040, 1048575]
    home = expanduser("~")
    db_dir = home + "/test/scripts/stats/sample-data/db/*.db"
    db_path = home + "/test/scripts/stats/sample-data/db"

    vps:list = get_vantage_points(get_filenames(db_dir))
    for vp in vps:
        print(vp)

    # Large data:
    #db_dir = home + "/db-storage/large-data/*.db"
    #db_path = home + "/db-storage/large-data/db-ubuntu-ams3-0-2023-01-19T23_00_25Z.db"

    # Test/small data:
    #db_dir = home + "/git/scripts/stats/sample-data/db/*.db"
    #db_path = home + "/git/scripts/stats/sample-data/db/db-ubuntu-fra1-0-2023-01-22T17_04_15Z.db"

    #df: pd.DataFrame = sq.load_single(db_path)
    #df: pd.DataFrame = sq.load_all(db_dir)
    #num_rows = get_num_rows(df)
    #print(f"{num_rows=}")

    #num_loops: int = filter.count_loops(df)
    # print(f"{num_loops=}")
    #num_cycles: int = filter.count_cycles(df)
    # print(f"{num_cycles=}")

    #print("Number of flow label changes in transit:")
    #num_path_flow_label_changes: int = filter.count_path_flow_label_changes(df)
    # print(f"{num_path_flow_label_changes=}")

    #print("Number of rows with flow label changes in transit:")
    # num_path_flow_label_changes: int = len(
    # filter.get_rows_with_path_flow_label_changes(df))
    # print(f"{num_path_flow_label_changes=}")

    #stats: TracerouteStatistics = create_stats(df)
    # print(repr(stats))
    #df = filter.remove_invalid_traces(df)

    #for flow_label in source_flow_labels:
        #print(f"Distribution of equal paths with flow label {flow_label}:")
        #dist = filter.get_distribution_of_equal_paths_to_destination(
            #df, flowlabel=flow_label)
        #plt.bar([str(i) for i in dist.index], dist)
        # print(dist.to_string())
        # plot.histogram(dist)


if __name__ == "__main__":
    main()
