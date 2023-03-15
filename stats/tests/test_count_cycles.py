import time
import pytest
import pandas as pd
from os.path import expanduser

home = expanduser("~")
db_name = "sample-200.csv"
db_location = home + "/git/scripts/stats/tests/sample-data/" + db_name

data: pd.DataFrame = pd.read_csv(db_location)


# def get_cycle_indices(df: pd.DataFrame) -> list:
# """
# Get a list containing the indices of all rows that contain one or more cycles in the dataset.
# """
# indices = list()
# for row_idx in df.index:
# hop_ip_list: list = get_hop_ip_list(df, row_idx)
# unique_list = get_unique_list_items(hop_ip_list)
# for item in unique_list:
# ip_count = hop_ip_list.count(item)
# if ip_count >= 2:
# if is_cycle(hop_ip_list):
# indices.append(row_idx)
# Uncomment this if we only want to count 1 cycle per row.
# break
# return indices


# def is_cycle(hop_ip_list: list) -> bool:
# """
# Checks whether there is a cycle in a given list of
# sequential ip addresses
# """
# for idx, ip in enumerate(hop_ip_list):
# for inner_ip in hop_ip_list[idx+2:]:
# if ip == inner_ip and ip != hop_ip_list[idx+1]:
# return True
# return False


# def get_unique_list_items(input: list) -> list:
# """
# Get a list containing only the unique values from the input list.
# """
# unique_list = list()
# for item in input:
# if item not in unique_list:
# unique_list.append(item)
# return unique_list


# def get_hop_ip_list(df: pd.DataFrame, row_idx: int) -> list:
# hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
# hop_ip_list: list = hop_ip_str.split(" ")
# return hop_ip_list


# Old, erronous function:
# def count_cycles(df: pd.DataFrame) -> int:
# """
# Count the number of cycles in the dataset. If there are multiple
# cycles in each row, each will be counted as a separate cycle.
# A cycle is where the same IP address appears twice, separated by
# at least one other IP address.
# """
# cycle_count = 0
# for row_idx in df.index:
# hop_ip_list: list = get_hop_ip_list(df, row_idx)
# unique_list = get_unique_list_items(hop_ip_list)
# for item in unique_list:
# ip_count = hop_ip_list.count(item)
# if ip_count >= 2:
# if is_cycle(hop_ip_list):
# cycle_count += 1
# print("Cycle list:")
# print(unique_list)
# time.sleep(1000)
# return cycle_count


# NEW (hopefully) fixed function:
def count_cycles(df: pd.DataFrame) -> int:
    """
    This function only gets 1 cycle per IP-address.
    For instance, if there is a IP-address list in the form [A, B, A, A, A],
    only 1 cycle would be counted.
    If there is a IP-address list in the form [A, B, A, A, A, B],
    it would count 2 cycles.
    """
    cycle_count = 0
    for row in df.itertuples():
        hop_ip_addresses = tuple(row[10].split())
        # hop_numbers = tuple(row[11].split())
        # columns = zip(hop_ip_addresses, hop_numbers)
        length = len(hop_ip_addresses)
        for idx, column in enumerate(hop_ip_addresses):
            i = idx
            # Incrementing by one to avoid comparing against the next IP-address (which would make it a loop)
            i += 1
            while i < length:
                if column == hop_ip_addresses[i]:
                    print("cycle detected")
                    cycle_count += 1
                    break
                else:
                    print("cycle not detected")
                i += 1
            time.sleep(1000)
    return cycle_count


def get_cycle_indices(df: pd.DataFrame) -> list:
    cycle_indices = list()
    for row in df.itertuples():
        break_out_flag = False
        hop_ip_addresses = tuple(row[10].split())
        length = len(hop_ip_addresses)
        for idx, column in enumerate(hop_ip_addresses):
            if break_out_flag:
                break
            i = idx
            # Incrementing by one to avoid comparing against the next IP-address (which would make it a loop)
            i += 1
            while i < length:
                if column == hop_ip_addresses[i]:
                    cycle_indices.append(idx)
                    break_out_flag = True
                    break
                i += 1
    return cycle_indices


    # print("Counting cycles")
    # num_cycles = count_cycles(data)
    # print(f"Num cycles: {num_cycles}")
    # print("Getting cycle indices")
    # cycle_indices = get_cycle_indices(data)
    # print(f"Cycle indices:\n{cycle_indices}")
count_cycles(data)


def f():
    return 3


def test_function():
    assert f() == 4
