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


def get_unique_list_items(input: list) -> list:
    """
    Get a list containing only the unique values from the input list.
    """
    unique_list = list()
    for item in input:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def get_hop_ip_list(df: pd.DataFrame, row_idx: int) -> list:
    hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
    hop_ip_list: list = hop_ip_str.split(" ")
    return hop_ip_list


def get_rows_with_path_flow_label_changes(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
    """
    indices = list()
    for row_idx in df.index:
        src_fl: str = str(df["SOURCE_FLOW_LABEL"].iloc[row_idx])
        ndf: str = df["HOP_RETURNED_FLOW_LABELS"].iloc[row_idx]
        flow_labels: list = ndf.split(" ")
        for val in flow_labels:
            if src_fl != val:
                indices.append(row_idx)
                break
    return indices


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


def get_invalid_traces_indices(df: pd.DataFrame):
    """
    Get a list containing the indicies of all rows
    with invalid traces.
    """
    loop_indices: list = get_loop_indices(df)
    cycle_indices: list = get_cycle_indices(df)
    fl_change_indices: list = get_rows_with_path_flow_label_changes(df)
    merged_list = loop_indices + cycle_indices + fl_change_indices
    # Remove duplicate entries
    merged_list = list(dict.fromkeys(merged_list))
    return merged_list


def find_sibling_indices_for_all(df: pd.DataFrame) -> list:
    """
    If one row is deemed to be invalid, we also have to remove
    its sibling row.
    """
    associated_rows = list()
    invalid_traces: list = get_invalid_traces_indices(df)
    for row_idx in invalid_traces:
        sibling_indices = find_sibling_indices_for_one(row_idx, df)
        # associated_rows.append(sibling_indices)
        associated_rows = associated_rows + sibling_indices
    return associated_rows


def find_sibling_indices_for_one(row_idx, df: pd.DataFrame) -> list:
    """
    Returns the indices (row-numbers) of a row's sibling.
    """
    indices = list()
    row_src_ip = df["SOURCE_IP"].iloc[row_idx]
    row_dst_ip = df["DESTINATION_IP"].iloc[row_idx]
    row_flow_label = df["SOURCE_FLOW_LABEL"].iloc[row_idx]
    for idx in df.index:
        if (df["SOURCE_IP"].iloc[idx] == row_src_ip) and (df["DESTINATION_IP"].iloc[idx] == row_dst_ip) and (df["SOURCE_FLOW_LABEL"].iloc[idx] == row_flow_label) and (idx != row_idx):
            indices.append(idx)
    return indices


def count_sibling_indices(df: pd.DataFrame) -> int:
    return len(find_sibling_indices_for_all(df))


result = count_sibling_indices(df)
print(result)
