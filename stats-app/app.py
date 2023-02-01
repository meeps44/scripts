from stats.definitions.classdefinitions import *
import stats.plot as splt
import stats.filter as filter
import stats.compare as scmp
import stats.sqlite_load as sq
import prettyprinter as pp
import glob
import pandas as pd


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


def get_distribution_of_equal_paths_to_destination(df: pd.DataFrame, flowlabel: int, destination_addr: str):
    """
    Get the number of paths 
    """
    if flowlabel == 0:
        df = df["time"] == "Dinner"
        eqp = df.value_counts()
        return eqp
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


def get_total_number_of_unique_vp_source_asns(df: pd.DataFrame):
    pass


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


def get_number_of_times_flowlabel_changed_in_transit(df: pd.DataFrame, vp: VantagePoint):
    if vp.ams3:
        sfl: pd.Series = df[['SOURCE_FLOW_LABEL']]
        dfl: pd.Series = df[['RECEIVED_FLOW_LABELS']]
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


def get_total_number_of_times_flowlabel_changed_in_transit(df: pd.DataFrame):
    sfl: pd.Series = df[['SOURCE_FLOW_LABEL']]
    dfl: pd.Series = df[['RECEIVED_FLOW_LABELS']]


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


# def get_unique_start_times(db_dir: str, source_flow_labels: list):
    # """
    # Get the unique values in the START_TIME column from all databases
    # in a directory, and combine to a single dataframe.
    # """
    #source_flow_labels = [0, 255, 1048575]
    #ls: list[str] = glob.glob(db_dir)
    #base: pd.DataFrame = pd.DataFrame()
    # for db_file in ls:
    #conn = filter.sqlite_init(db_file)
    #unique_start_times = filter.get_unique_start_times(conn)
    # for time in unique_start_times:
    # for fl in source_flow_labels:
    # df = filter.sqlite_exec(
    # conn, f"SELECT PATH_HASH FROM TRACEROUTE_DATA WHERE START_TIME={time} AND SOURCE_FLOW_LABEL={fl}")
    # base.concat(df)
    # return base


def create_stats(df: pd.DataFrame) -> TracerouteStatistics:
    stats = TracerouteStatistics()
    stats.num_rows_total = get_num_rows(df)
    stats.num_loops = filter.count_loops(df)
    stats.num_cycles = filter.count_cycles(df)
    stats.num_asns_traversed = get_total_number_of_asns_traversed(df)
    stats.num_fl_changes = get_total_number_of_times_flowlabel_changed_in_transit(
        df)
    return stats


def main():
    #db_dir = "/home/erlhap/test/python/paris-traceroute-filter/data/*.db"
    db_dir = "/home/erlend/git/scripts/stats-app/sample-data/db/*.db"
    db_path = "/home/erlend/git/scripts/stats-app/sample-data/db/db-ubuntu-fra1-0-2023-01-22T17_04_15Z.db"
    #db_dir = "/home/erlhap/test/scripts/stats-app/sample-data/db/*.db"
    source_flow_labels = [0, 255, 1048575]
    #start_times: pd.DataFrame = get_collective_unique_start_times(db_dir, source_flow_labels)
    #df: pd.DataFrame = sq.load_single(db_path)
    df: pd.DataFrame = sq.load_all(db_dir)
    print(df)
    #start_times: pd.DataFrame = filter.get_unique_start_times(df)
    #stats: TracerouteStatistics = create_stats(df)
    # print(repr(stats))
    #loop_list: list = filter.get_loops(df)
    #cycles_list: list = filter.get_cycles(df)
    #df = filter.remove_indices(loop_list)
    #df = filter.remove_indices(cycles_list)


if __name__ == "__main__":
    main()
