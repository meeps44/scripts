from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd

@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0

def print_stats(stats: TracerouteStatistics):
    pass

def get_path_flow_label_changes(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all rows where the flow label changed en-route.
    """
    pass

def remove_path_flow_label_changes(df: pd.DataFrame, indices: list):
    """
    Remove all rows where the flow label changed en-route.
    """
    pass

def get_loops(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all loops in the dataset.
    """
    pass

def remove_loops(indices: list):
    pass

def get_cycles(df: pd.DataFrame) -> list:
    """
    Get a list containing the indices of all cycles in the dataset.
    """
    pass
def remove_cycles(indices: list) -> list:
    pass

def get_unique_start_times(conn) -> list:
    df = sqlite_exec(conn, 'SELECT START_TIME FROM TRACEROUTE_DATA')
    return df["START_TIME"].unique()

def sqlite_init(filename: str):
    return connect(filename)

def sqlite_exec(conn, query) -> pd.DataFrame:
    return pd.read_sql(query, conn)

def main():
    source_flow_labels = [0, 255, 1048575]
    filepath = "/home/erlhap/test/python/paris-traceroute-filter/data/"
    filename = "db-ubuntu-ams3-0-2023-01-19T22_32_20Z.db"
    conn = sqlite_init(filepath + filename)
    unique_start_times = get_unique_start_times(conn)
    for time in unique_start_times:
        for fl in source_flow_labels:
            df = sqlite_exec(conn, f"SELECT PATH_HASH FROM TRACEROUTE_DATA WHERE START_TIME={time} AND SOURCE_FLOW_LABEL={fl}")
    print(df)


if __name__ == "__main__":
    main()
