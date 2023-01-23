from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0


def print_stats(stats: TracerouteStatistics):
    pass


def get_path_flow_label_changes(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
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


def count_loops(df: pd.DataFrame) -> int:
    """
    Count the number of loops in the dataset. If there are multiple 
    loops in each row, each will be counted as a separate loops.
    Loop defintion:
    If the same IP address appears twice or more in a row: we call this a loop.
    """
    nloops = 0
    for row_idx in df.index:
        hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
        hop_ip_list: list = hop_ip_str.split(" ")
        prev_ip = hop_ip_list[0]
        for idx, ip in enumerate(hop_ip_list):
            if idx != 0:
                if ip == prev_ip:
                    print("Loop detected!")
                    nloops = nloops + 1
            prev_ip = ip
    return nloops


def get_loops(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows that contain loops in the dataset.
    """
    indices = list()
    for row_idx in df.index:
        hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
        hop_ip_list: list = hop_ip_str.split(" ")
        prev_ip = hop_ip_list[0]
        for idx, ip in enumerate(hop_ip_list):
            if idx != 0:
                if ip == prev_ip:
                    print("Loop detected!")
                    indices.append(row_idx)
                    break
            prev_ip = ip
    return indices


def remove_indices(df: pd.DataFrame, indices: list):
    return df.drop(index=indices)


def count_cycles(df: pd.DataFrame) -> int:
    """
    Count the number of cycles in the dataset. If there are multiple 
    cycles in each row, each will be counted as a separate cycle.
    A cycle is where the same IP address appears twice, separated by 
    at least one other IP address.
    """
    count = 0
    for row_idx in df.index:
        hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
        hop_ip_list: list = hop_ip_str.split(" ")
        unique_list = get_unique(hop_ip_list)
        for item in unique_list:
            count = hop_ip_list.count(item)
            if count >= 2:
                count = count + 1
                # break # Uncomment this if we only want to count 1 cycle per row.
    return count


def get_unique(input: list) -> list:
    """
    Get a list containing only the unique values from the input list.
    """
    unique_list = list()
    for item in input:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def get_cycles(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows that contain one or more cycles in the dataset.
    """
    indices = list()
    for row_idx in df.index:
        hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
        hop_ip_list: list = hop_ip_str.split(" ")
        unique_list = get_unique(hop_ip_list)
        for item in unique_list:
            count = hop_ip_list.count(item)
            if count >= 2:
                indices.append(row_idx)
                break
    return indices


def get_unique_start_times(conn) -> list:
    df = sqlite_exec(conn, 'SELECT START_TIME FROM TRACEROUTE_DATA')
    return df["START_TIME"].unique()


def sqlite_init(filename: str):
    return connect(filename)


def sqlite_exec(conn, query) -> pd.DataFrame:
    return pd.read_sql(query, conn)


def main():
    stats = TracerouteStatistics()
    source_flow_labels = [0, 255, 1048575]
    filepath = "/home/erlhap/test/python/paris-traceroute-filter/data/"
    filename = "db-ubuntu-ams3-0-2023-01-19T22_32_20Z.db"
    conn = sqlite_init(filepath + filename)
    unique_start_times = get_unique_start_times(conn)
    for time in unique_start_times:
        for fl in source_flow_labels:
            df = sqlite_exec(
                conn, f"SELECT PATH_HASH FROM TRACEROUTE_DATA WHERE START_TIME={time} AND SOURCE_FLOW_LABEL={fl}")
    print(df)


if __name__ == "__main__":
    main()
