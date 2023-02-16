# import prettyprinter as pp
import pandas as pd
from lib.definitions.classdefinitions import *
import lib.plot as plot
import lib.filter as filter
import lib.compare as scmp
import lib.sqlite_load as sq
import logging
import glob
import re


# def create_hop_divergence_number_cdf(df: pd.DataFrame, flow_label: int, vantage_point: VantagePoint):
# pass


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
    stats.num_loops = count_loops(df)
    stats.num_loop_rows = 0
    stats.num_cycles = count_cycles(df)
    stats.num_cycle_rows = 0
    # stats.num_asns_traversed = get_asns_traversed(df)
    stats.num_fl_changes = len(
        get_rows_with_path_flow_label_changes(df))
    return stats


def get_total_number_of_loops_in_dataset(df: pd.DataFrame):
    return count_loops(df)


def get_num_rows(df: pd.DataFrame) -> int:
    """
    Get number of rows in the dataframe.
    """
    return len(df)


def list_compare(list1, list2) -> int:
    """
    Compare two ordered lists and get the index where they diverge.
    Returns None if the lists are equal.
    """
    max_len = max(len(list1), len(list2))
    try:
        for idx in range(max_len):
            if list1[idx] != list2[idx]:
                return idx  # incrementing by 1 since idx starts at 0
        # If we got this far, the lists are equal
        return None
    except IndexError:
        return idx


def create_list_of_lists(df: pd.DataFrame):
    pass


def hop_list_to_list_of_tuples(df: pd.DataFrame, row_number: int) -> list:
    """
    Converts one ["HOP_IP_ADDRESSES", "HOP_NUMBERS"]-entry (one row) into a 
    list of lists in the format [[ip, hop_number], [ip2, hop_number2], ...].
    Input: df[["HOP_IP_ADDRESSES", "HOP_NUMBERS"]]
    Output: list_of_lists
    """
    df = df[["HOP_IP_ADDRESSES",
             "HOP_NUMBERS"]].iloc[row_number]
    hop_ip_addresses_list = str(
        df.iloc[0]['HOP_IP_ADDRESSES']).split()
    hop_numbers_list = str(
        df.iloc[0]['HOP_NUMBERS']).split()
    list_of_tuples = list()
    for idx, val in enumerate(hop_ip_addresses_list):
        list_of_tuples.append(tuple((val, hop_numbers_list[idx])))
    return list_of_tuples


def get_max_len(list_of_lists: list) -> int:
    max_len = 0
    for item in list_of_lists:
        max_len = max(len(item), max_len)
    return max_len


def get_index_where_lists_diverge(list_of_lists: list) -> int:
    """
    In a set of n lists, get the first index where the lists diverge.
    E.g.:
    path1 = [1,2,3]
    path2 = [1,5,3]
    path3 = [1,2,4]
    The lists first differ at index 1.
    """
    max_len = get_max_len(list_of_lists)
    try:
        for idx in range(max_len):
            tmp = list_of_lists[0][idx]
            for li in list_of_lists[1:]:
                if tmp != li[idx]:
                    return idx
        return None
    except IndexError:
        return idx


def get_asns_traversed(df: pd.DataFrame) -> list:
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    asns_traversed: list[str] = list()
    for row in df:
        asns_traversed.append(row)


# def print_stats(stats: TracerouteStatistics):
    # pp.install_extras()
    # pp.pprint(stats)


def get_total_number_of_paths(df: pd.DataFrame, flowlabel: int):
    df = df[df["source_flow_label"] == flowlabel]
    return get_num_rows(df)


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
        # ndf: pd.Series = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        # flow_labels: list = ndf.to_list()
        ndf: str = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        flow_labels: list = ndf.split(" ")
        # hrfl: pd.DataFrame = ndf.iloc[[row_idx]]
        # flow_labels = ndf.values.tolist()
        # hrfl = ' '.join(hrfl_list)
        # hrfl: str = df['HOP_RETURNED_FLOW_LABELS'][row_idx]
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
        # ndf: pd.DataFrame = df["HOP_RETURNED_FLOW_LABELS"]
        # hrfl: pd.DataFrame = ndf.iloc[[row_idx]]
        # flow_labels = hrfl.values.tolist()
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
        # hop_ip_list: list = df["HOP_IP_ADDRESSES"].iloc[row_idx].tolist()
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        prev_ip: str = hop_ip_list[0]
        for ip in hop_ip_list[1:]:
            if ip == prev_ip:
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
