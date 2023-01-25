from enum import Enum
import stats.plot as plt
import stats.filter as fil
import stats.compare as cmp
import glob
from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0


class VantagePoint(Enum):
    ams3 = 1
    blr1 = 2
    fra1 = 3
    lon1 = 4
    nyc1 = 5
    sfo3 = 6
    sgp1 = 7
    tor1 = 8


def compare_path_hash(df: pd.DataFrame, flowlabel: int, start_time: int):
    """
    Compare the path hash of all paths in the dataset with the same START_TIME and SOURCE_FLOW_LABEL.
    Return the number of instances where the path stayed the same.
    """
    indices = list()
    src_fl: str = df['SOURCE_FLOW_LABEL']
    for row_idx in df.index:
        hrfl: str = df['HOP_RETURNED_FLOW_LABELS'][row_idx]
        flow_labels: list = hrfl.split(" ")
        for val in flow_labels:
            if src_fl != val:
                indices.append(row_idx)
                break
    return indices


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


def get_number_of_equal_paths(df: pd.DataFrame, flowlabel: int):
    pass


def get_hop_where_path_diverged(df: pd.DataFrame, flowlabel: int, vp: VantagePoint):
    pass


def get_total_hop_where_path_diverged(df: pd.DataFrame, flowlabel: int):
    pass


def get_total_number_of_unique_vp_source_asns():
    pass


def get_total_number_of_unique_destination_asns():
    pass


def get_total_number_of_traceroutes_performed():
    pass


def get_total_number_of_loops_in_dataset():
    pass


def get_number_of_loops_in_dataset_per_vp(vp: VantagePoint):
    pass


def get_number_of_times_flowlabel_changed_in_transit(vp: VantagePoint):
    pass


def get_total_number_of_times_flowlabel_changed_in_transit():
    pass


def get_percentage_of_time_path_was_equal(vp: VantagePoint):
    pass


def get_total_percentage_of_time_path_was_equal():
    pass


def get_number_of_asns_traversed(df: pd.DataFrame):
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    plt.histogram_plot(df)


def main():
    stats = TracerouteStatistics()
    source_flow_labels = [0, 255, 1048575]
    # Get all databases in directory.
    ls: list = glob.glob(
        "/home/erlhap/test/python/paris-traceroute-filter/data/*.db")
    for db_file in ls:
        conn = fil.sqlite_init(db_file)
        unique_start_times = fil.get_unique_start_times(conn)
        for time in unique_start_times:
            for fl in source_flow_labels:
                df = fil.sqlite_exec(
                    conn, f"SELECT PATH_HASH FROM TRACEROUTE_DATA WHERE START_TIME={time} AND SOURCE_FLOW_LABEL={fl}")
        print(df)


if __name__ == "__main__":
    main()
