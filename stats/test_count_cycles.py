from lib.definitions.classdefinitions import *
from lib.sqlite_load import *
import time
import pytest
import pandas as pd
from os.path import expanduser
import matplotlib.pyplot as plt

home = expanduser("~")
# db_name = "sample-200.csv"
# db_location = home + "/git/scripts/stats/tests/sample-data/" + db_name
# data: pd.DataFrame = pd.read_csv(db_location)

db_path = "/home/erlend/db-storage/large-data/" + Databases.ams
data: pd.DataFrame = load_single(db_path)


def get_all_unique_hop_ip_addresses(df: pd.DataFrame) -> set:
    unique_hop_ip_addresses = set()
    for row in df.itertuples():
        hop_ip_addresses = set(row[10].split())
        unique_hop_ip_addresses.update(hop_ip_addresses)
    return unique_hop_ip_addresses


def test_count_cycles(hop_ip_addresses: tuple) -> int:
    """
    This function only gets 1 cycle per IP-address.
    For instance, if there is a IP-address list in the form [A, B, A, A, A],
    only 1 cycle would be counted.
    If there is a IP-address list in the form [A, B, A, A, A, B],
    it would count 2 cycles.
    """
    cycle_count = 0
    length = len(hop_ip_addresses)
    for idx, column in enumerate(hop_ip_addresses):
        i = idx
        # Incrementing by one to avoid comparing against the next IP-address (which would make it a loop)
        i += 1
        while i < length:
            if column == hop_ip_addresses[i]:
                cycle_count += 1
                break
            i += 1
    return cycle_count


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
        length = len(hop_ip_addresses)
        for idx, column in enumerate(hop_ip_addresses):
            i = idx
            # Incrementing by one to avoid comparing against the next IP-address (which would make it a loop)
            i += 2
            while i < length:
                if column == hop_ip_addresses[i]:
                    # print("Cycle detected")
                    # print(f"{row=}")
                    # print(f"{row[0]=}")
                    # print(f"{idx=}\n{i=}")
                    # print(f"{column=}\n{hop_ip_addresses[i]=}")
                    # print(f"{idx=}\n{i=}")
                    # print(f"{hop_ip_addresses=}")
                    cycle_count += 1
                    # time.sleep(1000)
                    break
                i += 1
    return cycle_count


def get_cycle_hashes(df: pd.DataFrame) -> list:
    cycle_hashes = list()
    for row in df.itertuples():
        break_out_flag = False
        hop_ip_addresses = tuple(row[10].split())
        length = len(hop_ip_addresses)
        for idx, column in enumerate(hop_ip_addresses):
            if break_out_flag:
                break
            i = idx
            # Incrementing by one to avoid comparing against the next IP-address (which would make it a loop)
            i += 2
            while i < length:
                if column == hop_ip_addresses[i]:
                    cycle_hashes.append(row[8])
                    break_out_flag = True
                    break
                i += 1
    return cycle_hashes


def get_loop_rows(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows that contain loops in the dataset.
    """
    loop_indices = list()
    for row in df.itertuples():
        break_out_flag = False
        hop_ip_addresses = tuple(row[10].split())
        length = len(hop_ip_addresses)
        for idx, ip in enumerate(hop_ip_addresses):
            if break_out_flag:
                break
            i = idx
            i += 1
            while i < length:
                if ip == hop_ip_addresses[i]:
                    loop_indices.append(row[0])
                    break_out_flag = True
                    break
                i += 1
    return loop_indices


def get_cycle_rows(df: pd.DataFrame) -> list:
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
            i += 2
            while i < length:
                if column == hop_ip_addresses[i]:
                    cycle_indices.append(row[0])
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
test_data = ('fd00:0:1::266', '2604:a880:ffff:4:1::46', '2604:a880:ffff:4:1::34', '2604:a880:ffff:4:1::46', '2a01:3e0:30::35', '2a01:3e0:ff40:200::21', '2001:5a0:2000:500::22', '2001:5a0:2000:500::52', '2001:5a0:a00::32', '2001:470:0:387::2', '2001:470:0:387::2', '2001:5a0:40:300::65', '2001:1278:1::3ba', '2001:550:0:1000::9a36:3d5',
             '2001:550:0:1000::9a36:5076', '2001:550:0:1000::9a36:29ca', '2001:550:2:85::39:2', '2001:550:0:1000::9a36:29ca', '2001:1260:100:15::1e', '2001:1260:100:15::31', '2604:d600:ff00:5a::25', '2806:20d:50ff:75::2', '2001:1218:2000:4f0::1', '2001:1218:3000:2f0::a6', '2001:1218:420c::a', '2001:1218:1000:f0::9')
# cycle_count = test_count_cycles(test_data)
# print(f"cycle count: {cycle_count}")
cycle_count = count_cycles(data)
print(f"cycle count: {cycle_count}")
cycle_indices = get_cycle_rows(data)
print(f"len cycle indices: {len(cycle_indices)}")
number_of_rows = len(data.index)
print(f"number of rows: {number_of_rows}")
cycle_percentage = float(len(cycle_indices)) / float(number_of_rows)
print(f"cycle percentage: {cycle_percentage}")

loop_indices = get_loop_rows(data)
print(f"len loop rows: {len(loop_indices)}")

combined_indices = loop_indices + cycle_indices
unique_combined_indices = set(combined_indices)
print(
    f"number of rows that contain either a loop or a cycle: {len(unique_combined_indices)}")
# print(f"number of cycle rows that also contain a loop: {len(cycle_hashes)}")
# print(f"number of cycle rows that don't contain a loop: {len(cycle_hashes)}")


def get_loop_addresses(df: pd.DataFrame) -> list:
    loop_addresses = list()
    for row in df.itertuples():
        hop_ip_addresses = tuple(row[10].split())
        length = len(hop_ip_addresses)
        checked_addresses = list()
        for idx, ip in enumerate(hop_ip_addresses):
            i = idx
            i += 1
            while i < length:
                if ip == hop_ip_addresses[i] and (i, ip) not in checked_addresses:
                    checked_addresses.append((i, ip))
                    loop_addresses.append(ip)
                i += 1
    return loop_addresses


def get_cycle_addresses(df: pd.DataFrame) -> list:
    cycle_addresses = list()
    for row in df.itertuples():
        hop_ip_addresses = tuple(row[10].split())
        length = len(hop_ip_addresses)
        for idx, ip in enumerate(hop_ip_addresses):
            i = idx
            # Incrementing by one to avoid comparing against the next IP-address (which would make it a loop)
            i += 2
            while i < length:
                if ip == hop_ip_addresses[i]:
                    cycle_addresses.append(ip)
                    break
                i += 1
    return cycle_addresses


# print(f"Which IP-addresses loop?")
looping_addresses = get_loop_addresses(data)
# print(f"{looping_addresses}")
# plt.hist(looping_addresses)
# plt.show()
print(f"How many IP-addresses loop?")
print(f"{len(looping_addresses)}")
print(f"How many unique IP-addresses loop?")
print(f"{len(set(looping_addresses))}")

cycling_addresses = get_cycle_addresses(data)
# print(f"Which IP-addresses cycle?")
# print(f"{cycling_addresses}")
# plt.hist(cycling_addresses)
# plt.show()
print(f"How many IP-addresses cycle?")
print(f"{len(cycling_addresses)}")
print(f"How many unique IP-addresses cycle?")
print(f"{len(set(cycling_addresses))}")
print(f"How many unique hop IP-addresses are there in total?")
print(f"{len(get_all_unique_hop_ip_addresses(data))}")

# unique_hashes = data["PATH_HASH"].unique()
# print(f"total number of unique hashes in the dataset: {len(unique_hashes)}")


cycle_hashes = get_cycle_hashes(data)
print(f"number of hashes with a cycle: {len(cycle_hashes)}")
unique_cycle_hashes = set(cycle_hashes)
print(f"number of unique hashes with a cycle: {len(unique_cycle_hashes)}")
cycle_percentage = float(len(unique_cycle_hashes)) / float(number_of_rows)
print(f"cycle percentage: {cycle_percentage}")


def f():
    return 3


def test_function():
    assert f() == 4
