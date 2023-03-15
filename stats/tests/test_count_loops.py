import time
import pytest
import pandas as pd
from os.path import expanduser

home = expanduser("~")
db_name = "sample-200.csv"
db_location = home + "/git/scripts/stats/tests/sample-data/" + db_name

data: pd.DataFrame = pd.read_csv(db_location)


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
                print(f"row number: {row_idx}")
                print(f"ip: {ip}")
                print(f"prev_ip: {prev_ip}")
                time.sleep(100)
                nloops += 1
            prev_ip = ip
    return nloops


def get_hop_ip_list(df: pd.DataFrame, row_idx: int) -> list:
    hop_ip_str: str = df['HOP_IP_ADDRESSES'][row_idx]
    hop_ip_list: list = hop_ip_str.split(" ")
    return hop_ip_list


print("Counting loops")
num_loops = count_loops(data)
print(f"Num loops: {num_loops}")
print("Getting loop indices")
loop_indices = get_loop_indices(data)
print(f"Loop indices:\n{loop_indices}")


def f():
    return 3


def test_function():
    assert f() == 4
