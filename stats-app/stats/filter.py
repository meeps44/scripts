from stats.definitions.classdefinitions import *
from stats.sqlite_load import *
from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd
import logging


def get_distribution_of_equal_paths_to_destination(
        df: pd.DataFrame, flowlabel: int, unique_start_times: list) -> pd.Series:
    """
    Get the number of paths 
    """
    df = df[(df["SOURCE_FLOW_LABEL"] == str(flowlabel)) & (
        df["START_TIME"] == str(unique_start_times[0]))]
    df = df["PATH_HASH"]
    value_counts = df.value_counts()
    for start_time in unique_start_times[1:]:
        df = df[(df["SOURCE_FLOW_LABEL"] == str(flowlabel))
                & (df["START_TIME"] == str(start_time))]
        df = df["PATH_HASH"]
        eqp = df.value_counts()
        # concat
        value_counts = pd.concat([value_counts, eqp], axis=0)
    return value_counts


def count_path_flow_label_changes(df: pd.DataFrame) -> int:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
    """
    num_flow_label_changes: int = 0
    for row_idx in df.index:
        src_fl: str = str(df["SOURCE_FLOW_LABEL"].iloc[[row_idx]])
        ndf: pd.DataFrame = df["HOP_RETURNED_FLOW_LABELS"]
        hrfl: pd.DataFrame = ndf.iloc[[row_idx]]
        flow_labels = hrfl.values.tolist()
        #hrfl = ' '.join(hrfl_list)
        #hrfl: str = df['HOP_RETURNED_FLOW_LABELS'][row_idx]
        #flow_labels: list = hrfl.split(" ")
        for val in flow_labels:
            if src_fl != val:
                num_flow_label_changes = num_flow_label_changes + 1
    return num_flow_label_changes


def get_rows_with_path_flow_label_changes(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
    """
    indices = list()
    for row_idx in df.index:
        src_fl: str = str(df["SOURCE_FLOW_LABEL"].iloc[[row_idx]])
        ndf: pd.DataFrame = df["HOP_RETURNED_FLOW_LABELS"]
        hrfl: pd.DataFrame = ndf.iloc[[row_idx]]
        flow_labels = hrfl.values.tolist()
        #hrfl = ' '.join(hrfl_list)
        #hrfl: str = df['HOP_RETURNED_FLOW_LABELS'][row_idx]
        #flow_labels: list = hrfl.split(" ")
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
        hop_ip_list: str = df["HOP_IP_ADDRESSES"].iloc[[
            row_idx]].values.tolist()
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
    logging.debug(
        f"remove_indices: removed {len(indices)} rows from dataset")
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
        hop_ip_list: str = df["HOP_IP_ADDRESSES"].iloc[[
            row_idx]].values.tolist()
        unique_list = get_unique_list_items(hop_ip_list)
        for item in unique_list:
            count = hop_ip_list.count(item)
            if count >= 2:
                count = count + 1
                # break # Uncomment this if we only want to count 1 cycle per row.
    return count


def get_unique_list_items(input: list) -> list:
    """
    Get a list containing only the unique values from the input list.
    """
    unique_list = list()
    for item in input:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


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


def get_unique_start_times(df: pd.DataFrame):
    """
    Get the unique values in the START_TIME column from all databases 
    in a directory, and combine to a single dataframe.
    """
    return df["START_TIME"].unique()


def get_cycles(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows that contain one or more cycles in the dataset.
    """
    indices = list()
    for row_idx in df.index:
        hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
        hop_ip_list: list = hop_ip_str.split(" ")
        unique_list = get_unique_list_items(hop_ip_list)
        for item in unique_list:
            count = hop_ip_list.count(item)
            if count >= 2:
                indices.append(row_idx)
                break
    return indices


def main():
    pass


if __name__ == "__main__":
    main()
