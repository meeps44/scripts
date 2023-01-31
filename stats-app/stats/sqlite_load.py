import glob
import pandas as pd
from sqlite3 import connect

def get_unique_start_times(conn) -> list:
    df = sqlite_exec(conn, 'SELECT START_TIME FROM TRACEROUTE_DATA')
    return df["START_TIME"].unique()


def sqlite_init(filename: str):
    return connect(filename)


def sqlite_exec(conn, query) -> pd.DataFrame:
    return pd.read_sql(query, conn)

def load_single(conn, db: str):
    conn = sqlite_init(db)
    df = sqlite_exec(
        conn, f"SELECT * FROM TRACEROUTE_DATA")
    return df


def load_all(conn, db_dir: str) -> pd.DataFrame:
    ls: list[str] = glob.glob(db_dir)
    base: pd.DataFrame = pd.DataFrame()
    for db_file in ls:
        conn = sqlite_init(db_file)
        df = sqlite_exec(
            conn, f"SELECT * FROM TRACEROUTE_DATA")
        base.concat(df)
    return base


def main():
    print("sqlite_load main")

if __name__ == "__main__":
    main()
