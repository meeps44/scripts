import pandas as pd
from sqlite3 import connect

def get_unique_start_times(conn) -> list:
    df = sqlite_exec(conn, 'SELECT START_TIME FROM TRACEROUTE_DATA')
    return df["START_TIME"].unique()


def sqlite_init(filename: str):
    return connect(filename)


def sqlite_exec(conn, query) -> pd.DataFrame:
    return pd.read_sql(query, conn)

def main():
    print("sqlite_load main")

if __name__ == "__main__":
    main()
