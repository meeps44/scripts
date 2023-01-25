from enum import Enum
from filter import sqlite_init, sqlite_exec
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


def get_hop_where_path_diverged(df: pd.DataFrame, flowlabel: int):
    pass


def get_number_of_unique_vp_source_asns():
    pass


def get_number_of_unique_destination_asns():
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


def main():
    pass


if __name__ == "__main__":
    main()
