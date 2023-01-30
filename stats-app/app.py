from stats.definitions.classdefinitions import *
import stats.plot as splt
import stats.filter as sfil
import stats.compare as scmp
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

#def get_number_of_equal_paths_to_destination(df: pd.DataFrame, flowlabel: int, destination_addr: str):
    #"""
    #Get the number of paths 
    #"""
    #if flowlabel == 0:
        #df = df["time"] == "Dinner"
        #eqp = df.value_counts()
        #return eqp
    #elif flowlabel == 255:
        #pass
    #elif flowlabel == 65280:
        #pass
    #elif flowlabel == 983040:
        #pass
    #elif flowlabel == 1048575:
        #pass

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


def get_total_number_of_traceroutes_performed(df: pd.DataFrame):
    """
    Get number of rows in the dataframe.
    """
    return len(df)


def get_total_number_of_loops_in_dataset(df: pd.DataFrame):
    return sfil.count_loops(df)


def get_number_of_loops_in_dataset_per_vp(df: pd.DataFrame, vp: VantagePoint):
    if vp.ams3:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.blr1:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.fra1:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.lon1:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.nyc1:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.sfo3:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.sgp1:
        df = df['test']
        return sfil.count_loops(df)
    elif vp.tor1:
        df = df['test']
        return sfil.count_loops(df)


def get_number_of_times_flowlabel_changed_in_transit(df: pd.DataFrame, vp: VantagePoint):
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


def get_total_number_of_times_flowlabel_changed_in_transit(df: pd.DataFrame):
    pass


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


def get_number_of_asns_traversed(df: pd.DataFrame):
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    splt.histogram_plot(df)


def print_stats(stats: TracerouteStatistics):
    pp.install_extras()
    pp.pprint(stats)


def main():
    stats = TracerouteStatistics()
    source_flow_labels = [0, 255, 1048575]
    # Get all databases in directory.
    ls: list[str] = glob.glob(
        "/home/erlhap/test/python/paris-traceroute-filter/data/*.db")
    for db_file in ls:
        conn = sfil.sqlite_init(db_file)
        unique_start_times = sfil.get_unique_start_times(conn)
        for time in unique_start_times:
            for fl in source_flow_labels:
                df = sfil.sqlite_exec(
                    conn, f"SELECT PATH_HASH FROM TRACEROUTE_DATA WHERE START_TIME={time} AND SOURCE_FLOW_LABEL={fl}")
        print(df)


if __name__ == "__main__":
    main()
