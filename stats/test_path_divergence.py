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


def get_unique_routers_where_a_path_change_occurred(df: pd.DataFrame) -> list:
    """
    Return a list of all routers (IP-addresses) where a change in path
    was detected.
    """
    unique_destination_addresses: list = get_unique_destination_addresses(df)
    for dst in unique_destination_addresses:
        dst_df = df[(df["SOURCE_FLOW_LABEL"] == flow_label)
                    & (df["DESTINATION_IP"] == dst)]


def get_divergence_hop_ip(df: pd.DataFrame) -> str:
    """
    Compare two rows and get the hop IP where they diverge.
    """
    dst_df = df[(df["SOURCE_FLOW_LABEL"] == flow_label)
                & (df["DESTINATION_IP"] == dst)]
    print(f"dst_df len={len(dst_df.index)}")

    # Setup: creating the combined columns, represented as a list of tuples
    zipped_list = list()
    for row in dst_df.itertuples():
        hop_ip_addresses = row[10].split()
        hop_numbers = row[11].split()
        zipped = list(zip(hop_ip_addresses, hop_numbers, strict=True))
        zipped_list.append(zipped)

    # Compare the items in the two lists
    longest_list_len = get_length_of_longest_list(zipped_list)
    for i in longest_list_len:
        if zipped_list[0][i] != zipped_list[1][i]:
            if i != 0:
                # We are returning the previous IP (the last IP that was equal),
                # as we are assuming that this is the load balancer that caused the
                # paths to diverge.
                return zipped_list[0][i-1][0]
            else:
                # If the paths diverge at the first hop, we return the hop IP
                # of the first hop.
                return zipped_list[0][i][0]
                # return (zipped_list[0][i-1][0], zipped_list[0][i-1][0])
    # If we got this far, the lists are equal
    return None


def get_length_of_longest_list(list_of_lists: list) -> int:
    """
    Get the length of the longest list in list_of_lists
    """
    longest_list_len = 0
    for lst in list_of_lists:
        if len(lst) > longest_list_len:
            longest_list_len = len(lst)
    return longest_list_len
