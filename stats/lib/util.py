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


def get_filenames(db_dir: str) -> list:
    ls: list = glob.glob(db_dir)
    return ls


def get_vantage_points(filenames: list) -> list:
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


def get_hop_number_where_paths_diverged(df: pd.DataFrame, flowlabel: int, destination_address: str):
    # First check if the paths are equal by comparing the hash
    if something:
        print("Paths are equal!")
        return None
    # If we are here, the paths are not equal:
    path1 = list()  # list of (ip, hop_number)-tuples
    path2 = list()  # list of (ip, hop_number)-tuples
    try:
        for idx, tup in enumerate(path1):
            if tup != path2[idx]:
                return idx+1  # incrementing by 1 since idx starts at 0
    except IndexError:
        return idx


def get_asns_traversed(df: pd.DataFrame) -> list:
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    asns_traversed: list[str] = list()
    for row in df:
        asns_traversed.append(row)


def print_stats(stats: TracerouteStatistics):
    pp.install_extras()
    pp.pprint(stats)


def get_total_number_of_equal_paths(df: pd.DataFrame, flowlabel: int):
    pass


def get_total_number_of_unequal_paths(df: pd.DataFrame, flowlabel: int):
    pass


def get_value_counts(df: pd.DataFrame, flowlabel: int) -> pd.Series:
    """
    Get the number of paths 
    NOTE: df must be specific to a vantage point (not a cumulative df)
    """
    unique_destination_addresses: list = get_unique_destination_addresses(df)
    start_df: pd.DataFrame = df[(df["SOURCE_FLOW_LABEL"] == flowlabel) & (
        df["DESTINATION_IP"] == str(unique_destination_addresses[0]))]
    base: pd.Series = start_df["PATH_HASH"].value_counts()
    for addr in unique_destination_addresses[1:]:
        next_df: pd.DataFrame = df[(df["SOURCE_FLOW_LABEL"] == flowlabel)
                                   & (df["DESTINATION_IP"] == str(addr))]
        overlay: pd.Series = next_df["PATH_HASH"].value_counts()
        base = pd.concat([base, overlay], axis=0)
    logging.info(f"base value_counts:\n{base.value_counts().to_string()}")
    return base


def get_distribution_of_equal_paths_to_destination(
        df: pd.DataFrame, flowlabel: int) -> pd.Series:
    """
    Get the number of paths 
    NOTE: df must be specific to a vantage point (not a cumulative df)
    """
    unique_destination_addresses: list = get_unique_destination_addresses(df)
    start_df: pd.DataFrame = df[(df["SOURCE_FLOW_LABEL"] == flowlabel) & (
        df["DESTINATION_IP"] == str(unique_destination_addresses[0]))]
    base: pd.Series = start_df["PATH_HASH"].value_counts()
    for addr in unique_destination_addresses[1:]:
        next_df: pd.DataFrame = df[(df["SOURCE_FLOW_LABEL"] == flowlabel)
                                   & (df["DESTINATION_IP"] == str(addr))]
        overlay: pd.Series = next_df["PATH_HASH"].value_counts()
        base = pd.concat([base, overlay], axis=0)
    logging.info(f"base value_counts:\n{base.value_counts().to_string()}")
    return base.value_counts()


def count_path_flow_label_changes(df: pd.DataFrame) -> int:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
    """
    num_flow_label_changes: int = 0
    for row_idx in df.index:
        src_fl: str = str(df["SOURCE_FLOW_LABEL"].iloc[row_idx])
        print(
            f"Source flow label: {src_fl}\nSource flow label type:{type(src_fl)}")
        #ndf: pd.Series = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        #flow_labels: list = ndf.to_list()
        ndf: str = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        flow_labels: list = ndf.split(" ")
        #hrfl: pd.DataFrame = ndf.iloc[[row_idx]]
        #flow_labels = ndf.values.tolist()
        #hrfl = ' '.join(hrfl_list)
        #hrfl: str = df['HOP_RETURNED_FLOW_LABELS'][row_idx]
        print("Hop flow labels:")
        for val in flow_labels:
            print(val)
            (print(f"type: {type(val)}"))
            if src_fl != val:
                num_flow_label_changes += 1
    return num_flow_label_changes


def get_rows_with_path_flow_label_changes(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
    """
    indices = list()
    for row_idx in df.index:
        src_fl: str = str(df["SOURCE_FLOW_LABEL"].iloc[row_idx])
        #ndf: pd.DataFrame = df["HOP_RETURNED_FLOW_LABELS"]
        #hrfl: pd.DataFrame = ndf.iloc[[row_idx]]
        #flow_labels = hrfl.values.tolist()
        ndf: str = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        flow_labels: list = ndf.split(" ")
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
        #hop_ip_list: list = df["HOP_IP_ADDRESSES"].iloc[row_idx].tolist()
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        prev_ip: str = hop_ip_list[0]
        for ip in hop_ip_list[1:]:
            if ip == prev_ip:
                print("Loop detected!")
                nloops += 1
            prev_ip = ip
    return nloops


def get_hop_ip_list(df: pd.DataFrame, row_idx: int) -> list:
    hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
    hop_ip_list: list = hop_ip_str.split(" ")
    return hop_ip_list


def get_loop_indices(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows that contain loops in the dataset.
    """
    indices = list()
    for row_idx in df.index:
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        prev_ip = hop_ip_list[0]
        for idx, ip in enumerate(hop_ip_list):
            if idx != 0:
                if ip == prev_ip:
                    print("Loop detected!")
                    indices.append(row_idx)
                    break
            prev_ip = ip
    return indices


def count_cycles(df: pd.DataFrame) -> int:
    """
    Count the number of cycles in the dataset. If there are multiple 
    cycles in each row, each will be counted as a separate cycle.
    A cycle is where the same IP address appears twice, separated by 
    at least one other IP address.
    """
    cycle_count = 0
    for row_idx in df.index:
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        unique_list = get_unique_list_items(hop_ip_list)
        for item in unique_list:
            ip_count = hop_ip_list.count(item)
            if ip_count >= 2:
                if is_cycle(hop_ip_list):
                    cycle_count += 1
    return cycle_count


def is_cycle(hop_ip_list: list) -> bool:
    """
    Checks whether there is a cycle in a given list of 
    sequential ip addresses
    """
    for idx, ip in enumerate(hop_ip_list):
        for inner_ip in hop_ip_list[idx+2:]:
            if ip == inner_ip and ip != hop_ip_list[idx+1]:
                return True
    return False


def count_cycles_2(hop_ip_list: list) -> int:
    """
    Counts the number of cycles in a given list of 
    sequential ip addresses.
    """
    num_cycles: int = 0
    for idx, ip in enumerate(hop_ip_list):
        if ip in hop_ip_list[idx+2:] and ip != hop_ip_list[idx+1]:
            num_cycles += 1
    return num_cycles


def get_unique_list_items(input: list) -> list:
    """
    Get a list containing only the unique values from the input list.
    """
    unique_list = list()
    for item in input:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def get_unique_start_times(df: pd.DataFrame) -> list:
    """
    Get the unique values in the START_TIME column from all databases 
    in a directory, and combine to a single dataframe.
    """
    return df["START_TIME"].unique().tolist()


def get_unique_destination_addresses(df: pd.DataFrame) -> list:
    """
    Get the unique values in the START_TIME column from all databases 
    in a directory, and combine to a single dataframe.
    """
    return df["DESTINATION_IP"].unique().tolist()


def get_cycle_indices(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows that contain one or more cycles in the dataset.
    """
    indices = list()
    # for row_idx in df.index:
    #hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
    #hop_ip_list: list = hop_ip_str.split(" ")
    #unique_list = get_unique_list_items(hop_ip_list)
    # for item in unique_list:
    #count = hop_ip_list.count(item)
    # if count >= 2:
    # indices.append(row_idx)
    # break
    # return indices
    for row_idx in df.index:
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        unique_list = get_unique_list_items(hop_ip_list)
        for item in unique_list:
            ip_count = hop_ip_list.count(item)
            if ip_count >= 2:
                if is_cycle(hop_ip_list):
                    indices.append(row_idx)
                    # Uncomment this if we only want to count 1 cycle per row.
                    break
    return indices
