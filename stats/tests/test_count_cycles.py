from lib.definitions.classdefinitions import *
from lib.sqlite_load import *
import time
import pytest
import pandas as pd
from os.path import expanduser

home = expanduser("~")
# db_name = "sample-200.csv"
# db_location = home + "/git/scripts/stats/tests/sample-data/" + db_name
# data: pd.DataFrame = pd.read_csv(db_location)

db_path = "/home/erlend/db-storage/large-data/" + Databases.ams
data: pd.DataFrame = load_single(db_path)


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
print(f"total row len: {len(data.index)}")


def f():
    return 3


def test_function():
    assert f() == 4
