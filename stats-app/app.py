from stats.definitions.classdefinitions import *
import stats.plot as plot
import stats.filter as filter
import stats.compare as scmp
import stats.sqlite_load as sq
import prettyprinter as pp
import glob
import pandas as pd
import logging


def get_number_of_instances_where_path_stayed_consistent(df: pd.DataFrame, flowlabel: int):
    if flowlabel == 0:
        pass
    elif flowlabel == 255:
        pass
    elif flowlabel == 65280:
        pass
    elif flowlabel == 983040:
        pass
    elif flowlabel == 1048575:
        pass


# def get_number_of_equal_paths_to_destination(df: pd.DataFrame, flowlabel: int, destination_addr: str):
    # """
    # Get the number of paths
    # """
    # if flowlabel == 0:
        #df = df["time"] == "Dinner"
        #eqp = df.value_counts()
        # return eqp
    # elif flowlabel == 255:
        # pass
    # elif flowlabel == 65280:
        # pass
    # elif flowlabel == 983040:
        # pass
    # elif flowlabel == 1048575:
        # pass


def get_total_number_of_equal_paths(df: pd.DataFrame):
    pass


def get_hop_where_path_diverged(df: pd.DataFrame, flowlabel: int, vp: VantagePoint):
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


def get_total_hop_where_path_diverged(df: pd.DataFrame, flowlabel: int):
    pass


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


def get_number_of_loops_in_dataset_per_vp(df: pd.DataFrame, vp: VantagePoint):
    if vp.ams3:
        df = df['test']
        return filter.count_loops(df)
    elif vp.blr1:
        df = df['test']
        return filter.count_loops(df)
    elif vp.fra1:
        df = df['test']
        return filter.count_loops(df)
    elif vp.lon1:
        df = df['test']
        return filter.count_loops(df)
    elif vp.nyc1:
        df = df['test']
        return filter.count_loops(df)
    elif vp.sfo3:
        df = df['test']
        return filter.count_loops(df)
    elif vp.sgp1:
        df = df['test']
        return filter.count_loops(df)
    elif vp.tor1:
        df = df['test']
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


# def get_number_of_asns_traversed(df: pd.DataFrame):
def get_number_of_asns_traversed(df: pd.DataFrame, vp: VantagePoint):
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    number_of_asns: list = list()
    for row in df:
        number_of_asns.append()
    splt.histogram_plot(df)


def get_total_number_of_asns_traversed(df: pd.DataFrame):
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    number_of_asns: list = list()
    for row in df:
        number_of_asns.append()
    splt.histogram_plot(df)


def print_stats(stats: TracerouteStatistics):
    pp.install_extras()
    pp.pprint(stats)


def create_stats(df: pd.DataFrame) -> TracerouteStatistics:
    stats = TracerouteStatistics()
    stats.num_rows_total = get_num_rows(df)
    stats.num_loops = filter.count_loops(df)
    stats.num_cycles = filter.count_cycles(df)
    stats.num_asns_traversed = get_total_number_of_asns_traversed(df)
    stats.num_fl_changes = filter.count_path_flow_label_changes(
        filter.get_path_flow_label_changes(df))
    return stats


def main():
    #db_dir = "/home/erlhap/test/scripts/scripts/stats-app/sample-data/db/*.db"
    #db_path = "/home/erlhap/test/scripts/scripts/stats-app/sample-data/db"
    db_dir = "/home/erlend/git/scripts/stats-app/sample-data/db/*.db"
    db_path = "/home/erlend/git/scripts/stats-app/sample-data/db/db-ubuntu-fra1-0-2023-01-22T17_04_15Z.db"
    source_flow_labels = [0, 255, 65280, 983040, 1048575]
    #start_times: pd.DataFrame = get_collective_unique_start_times(db_dir, source_flow_labels)
    #df: pd.DataFrame = sq.load_single(db_path)
    df: pd.DataFrame = sq.load_all(db_dir)
    print("Hop returned flow labels:")
    ndf = df["HOP_RETURNED_FLOW_LABELS"]
    dflist = ndf.iloc[[0]].values.tolist()
    for item in dflist:
        print(str(item))
    print("src fl:")
    dflist = df["SOURCE_FLOW_LABEL"].iloc[[0]].values.tolist()
    for item in dflist:
        print(str(item))

    num_loops: int = filter.count_loops(df)
    print(f"{num_loops=}")
    num_cycles: int = filter.count_cycles(df)
    print(f"{num_cycles=}")

    print("Number of flow label changes in transit:")
    num_path_flow_label_changes: int = filter.count_path_flow_label_changes(df)
    print(f"{num_path_flow_label_changes=}")

    #start_times: pd.DataFrame = filter.get_unique_start_times(df)
    #stats: TracerouteStatistics = create_stats(df)
    # print(repr(stats))

    # Remove rows containing loops
    logging.debug("Removing loops")
    df = filter.remove_indices(df, filter.get_loops(df))
    # Remove rows containing cycles
    logging.debug("Removing cycles")
    df = filter.remove_indices(df, filter.get_cycles(df))
    # Remove rows with flow label changes
    logging.debug("Removing rows with flow label changes")
    df = filter.remove_indices(df,
                               filter.get_rows_with_path_flow_label_changes(df))

    print("Distribution of equal paths with flow label 0:")
    dist = filter.get_distribution_of_equal_paths_to_destination(
        df, flowlabel=FlowLabels.FL_0)
    plot.histogram(dist)
    print("Distribution of equal paths with flow label 255:")
    print("Distribution of equal paths with flow label 0:")
    print("Distribution of equal paths with flow label 0:")
    print("Distribution of equal paths with flow label 0:")


if __name__ == "__main__":
    main()
