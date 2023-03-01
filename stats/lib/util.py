import numpy as np
import pandas as pd
from lib.definitions.classdefinitions import *
import seaborn as sns
import matplotlib.pyplot as plt
import lib.plot as stats_plt
import lib.filter as filter
import lib.compare as scmp
import lib.sqlite_load as sq
import logging
import glob
import re
import numpy as np


def get_flow_label_change_hop_ip_distribution(df: pd.DataFrame, flow_label: np.int64) -> list:
    """
    NB! Do not use. Is buggy.
    Get a distribution of the hop IP-address where a change in flow label was detected.
    """
    hop_ip_distribution = list()
    # indices = get_rows_with_path_flow_label_changes(df)
    # print(f"indices len: {len(indices)}")

    for row_idx in df.index:
        row: pd.Series = df.iloc[row_idx]
        src_fl = row["SOURCE_FLOW_LABEL"]
        if src_fl != flow_label:
            continue
        flow_labels_str: str = row["HOP_RETURNED_FLOW_LABELS"]
        flow_labels: list = flow_labels_str.split()
        hop_ip_addresses_str: str = row["HOP_IP_ADDRESSES"]
        hop_ip_addresses: list = hop_ip_addresses_str.split()
        hop_numbers_str: str = row["HOP_NUMBERS"]
        hop_numbers: list = hop_numbers_str.split()
        for hop_idx, hop_fl in enumerate(flow_labels):
            if src_fl != hop_fl:
                # if we want a tuple:
                # hop_ip_distribution.append(tuple(hop_ip_addresses[hop_idx], hop_numbers[hop_idx]))
                hop_ip_distribution.append(hop_ip_addresses[hop_idx])
    return hop_ip_distribution


def get_cycle_ip_addresses(df: pd.DataFrame) -> list:
    """
    Count the number of cycles in the dataset. If there are multiple 
    cycles in each row, each will be counted as a separate cycle.
    A cycle is where the same IP address appears twice, separated by 
    at least one other IP address.
    """
    cycle_ip_addresses = list()
    for row_idx in df.index:
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        unique_list = get_unique_list_items(hop_ip_list)
        for ip in unique_list:
            ip_count = hop_ip_list.count(ip)
            if ip_count >= 2:
                if is_cycle(hop_ip_list):
                    cycle_ip_addresses.append(ip)
    return cycle_ip_addresses


def get_loop_ip_addresses(df: pd.DataFrame) -> list:
    """
    Get a list of the loops in the dataset. If there are multiple 
    loops in each row, each will be counted as a separate loops.
    Loop defintion:
    If the same IP address appears twice or more in a row: we call this a loop.
    """
    loop_ip_addresses = list()
    for row_idx in df.index:
        hop_ip_list: list = get_hop_ip_list(df, row_idx)
        prev_ip: str = hop_ip_list[0]
        for ip in hop_ip_list[1:]:
            if ip == prev_ip:
                loop_ip_addresses.append(ip)
            prev_ip = ip
    return loop_ip_addresses


def count_invalid_traces(df: pd.DataFrame) -> int:
    """
    Count traces containing loops, cycles and flow label values
    that changed in-transit.
    """
    loop_indices: list = get_loop_indices(df)
    cycle_indices: list = get_cycle_indices(df)
    fl_change_indices: list = get_rows_with_path_flow_label_changes(df)
    merged_list = loop_indices + cycle_indices + fl_change_indices
    # Remove duplicate entries
    merged_list = list(dict.fromkeys(merged_list))
    return len(merged_list)


def get_num_fl_changes_rows(df: pd.DataFrame) -> int:
    return len(get_rows_with_path_flow_label_changes(df))


def get_num_loop_rows(df: pd.DataFrame) -> int:
    return len(get_loop_indices(df))


def get_num_cycle_rows(df: pd.DataFrame) -> int:
    return len(get_cycle_indices(df))


def create_equal_paths_distribution(df: pd.DataFrame, flow_label: int, vantage_point: VantagePoint):
    """
    Create a bar plot of the distribution of equal paths to
    each destination.
    """
    dist = get_distribution_of_equal_paths_to_destination(
        df, flowlabel=flow_label)
    fig, ax = plt.subplots()
    bars = ax.bar([str(i) for i in dist.index], dist)
    ax.bar_label(bars)
    plt.title(f"Vantage point: {vantage_point} \nFlow label: {flow_label}")


def create_hop_divergence_number_cdf(df: pd.DataFrame, flow_label: int, vantage_point: VantagePoint):
    divergence_data = list()
    unique_destination_addresses: list = get_unique_destination_addresses(df)
    # print(f"unique_destination_addresses len: {len(unique_destination_addresses)}")
    for dst in unique_destination_addresses:
        dst_df = df[(df["SOURCE_FLOW_LABEL"] == flow_label)
                    & (df["DESTINATION_IP"] == dst)]
        list_of_lists = create_list_of_lists(dst_df)
        # print(f"{list_of_lists=}")
        # divergence_data.append( util.get_index_where_lists_diverge(list_of_lists) )
        divergence_data.append(
            get_lowest_hop_number_where_lists_diverge(list_of_lists))
        # print("destination: " + dst)
        # print("flow label: " + str( flow_label ))
        # print("get_distribution_of_number_of_asn_hops_to_destination:" + str(get_distribution_of_number_of_asn_hops_to_destination(
        # df, flow_label, dst)))
    # print(f"{divergence_data=}")
    # print("Number of traces to the same destination with the same flow label that did not diverge:")
    ndiv_count = divergence_data.count(None)
    # print(f"{ ndiv_count= }")
    # print(f"Total number of traces in divergence dataset:")
    # print(f"{ len(divergence_data)= }")
    # Remove None values before plotting CDF
    res = [int(i) for i in divergence_data if i != None]
    # print(f"{res=}")
    # Plot CDF
    sns.ecdfplot(data=res, label="Divergence number")
    plt.legend()
    plt.show()


def create_list_of_lists(df: pd.DataFrame) -> list:
    """
    Create a list of hop_lists with hop number N to a single
    destination address in the format:
    [[hop_number1, hop_number2, ...], [hop_number1, hop_number2, ...], ...]
    """
    list_of_lists = list()
    # print("create_list_of_lists")
    # print("df.index len: ", len(df.index))
    df = df.reset_index()  # make sure indexes pair with number of rows
    for row in df.itertuples():
        # hop_list = hop_list_to_list_of_tuples(df, idx)
        hop_list = hop_list_to_list_of_tuples(row)
        # print(f"{hop_list=}")
        list_of_lists.append(hop_list)
        # print(f"{list_of_lists=}")
    return list_of_lists


def get_all_unique_asns_in_dataset(df: pd.DataFrame) -> list:
    """
    Get the unique values in the START_TIME column from all databases 
    in a directory, and combine to a single dataframe.
    """
    src_df = df["SOURCE_ASN"].unique()
    dst_df = df["DESTINATION_ASN"].unique()
    hop_asn_list = list()
    for row_idx in df.index:
        hal: list = str(df["HOP_ASNS"].iloc[row_idx]).split()
        for asn in hal:
            hop_asn_list.append(asn)
    unique = list(set(src_df.tolist() + dst_df.tolist() + hop_asn_list))
    return unique


def get_distribution_of_number_of_asn_hops_to_destination(df: pd.DataFrame, flow_label: int, destination: str) -> pd.Series:
    """
    Get a distribution of the number of ASN hops to a destination address 
    with the given flow label.
    Can be plotted to a histogram.
    """
    dst_df = df[(df["SOURCE_FLOW_LABEL"] == flow_label)
                & (df["DESTINATION_IP"] == destination)]
    num_asn_hops: list = list()
    for row in dst_df.itertuples():
        hop_asn_list: list = list()
        hal: list = str(row[13]).split()
        for asn in hal:
            print(f"{asn=}")
            if asn != "NULL":
                hop_asn_list.append(asn)
        num_asn_hops.append(len(hop_asn_list))
    return pd.Series(num_asn_hops).value_counts()


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
    """
    Create a new TracerouteStatistics-object and initialize
    it with values from the given dataframe.
    """
    stats = TracerouteStatistics()
    stats.num_rows_total = get_num_rows(df)
    stats.num_loops = count_loops(df)
    stats.num_loop_rows = get_num_loop_rows(df)
    stats.num_cycles = count_cycles(df)
    stats.num_cycle_rows = get_num_cycle_rows(df)
    stats.num_unique_asns_in_dataset = len(get_all_unique_asns_in_dataset(df))
    stats.num_fl_changes = len(
        get_rows_with_path_flow_label_changes(df))
    stats.num_fl_change_rows = get_num_fl_changes_rows(df)
    stats.num_invalid_rows = count_invalid_traces(df)
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


def hop_list_to_list_of_tuples(row) -> list:
    """
    Converts one ["HOP_IP_ADDRESSES", "HOP_NUMBERS"]-entry (one row) into a 
    list of lists in the format [[ip, hop_number], [ip2, hop_number2], ...].
    Input: df[["HOP_IP_ADDRESSES", "HOP_NUMBERS"]]
    Output: list_of_lists
    """
    # print(f"{row=}")
    hop_ip_addresses_list = str(row[11]).split()
    # print(f"{hop_ip_addresses_list=}")
    hop_numbers_list = str(row[12]).split()
    # print(f"{hop_numbers_list=}")
    list_of_tuples = list()
    for idx, val in enumerate(hop_ip_addresses_list):
        # print(f"{idx=}")
        # print(f"{val=}")
        # print(f"{hop_numbers_list[idx]=}")
        list_of_tuples.append(tuple((val, hop_numbers_list[idx])))
    # print(f"{list_of_tuples=}")
    return list_of_tuples


def get_max_len(list_of_lists: list) -> int:
    """
    Get the length of the longest list out of N lists.
    """
    max_len = 0
    for item in list_of_lists:
        max_len = max(len(item), max_len)
    return max_len


def get_lowest_hop_number_where_lists_diverge(list_of_lists: list) -> int:
    """
    Assumes:
    list_of_lists contains only rows to 1 destination with only 1 constant 
    flow label.

    Get the smallest hop number where a list divergence was detected.
    list_of_lists is a list in the format:
    [[(hop_address1, hop_number1), (hop_address2, hop_number2), ...], 
    [(hop_address1, hop_number1), (hop_address2, hop_number2), ...], ...]
    """
    max_len = get_max_len(list_of_lists)
    for idx in range(max_len):
        tmp = list_of_lists[0][idx]
        for li in list_of_lists[1:]:
            if tmp != li[idx]:
                hop_numbers = list()
                for i in list_of_lists:
                    # Get the second item in the tuple, aka the hop_number
                    hop_numbers.append(i[idx][1])
                return min(hop_numbers)
    # If we got this far, the hops did not diverge
    return None


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


def get_asns_traversed(df: pd.Series) -> list:
    # Insert code to be done before this #
    # Data from the DataFrame should be a pd.Series
    asns_traversed: list[str] = list()
    for row in df:
        asns_traversed.append(row)


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
        ndf: str = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        flow_labels: list = ndf.split(" ")
        for val in flow_labels:
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


# def count_cycles_2(hop_ip_list: list) -> int:
    # """
    # Counts the number of cycles in a given list of
    # sequential ip addresses.
    # """
    # num_cycles: int = 0
    # for idx, ip in enumerate(hop_ip_list):
    # if ip in hop_ip_list[idx+2:] and ip != hop_ip_list[idx+1]:
    # num_cycles += 1
    # return num_cycles


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
