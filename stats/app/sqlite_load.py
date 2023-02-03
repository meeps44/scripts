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


def load_single(db: str):
    """
    Convenience function loads all rows
    from a single database in a directory into a single pandas
    DataFrame.
    """
    conn = sqlite_init(db)
    df = sqlite_exec(
        conn, f"SELECT * FROM TRACEROUTE_DATA")
    return df


def load_all(db_dir: str) -> pd.DataFrame:
    """
    Convenience function that loads all rows
    from all databases in a directory into a single pandas
    DataFrame.
    """
    ls: list[str] = glob.glob(db_dir)
    print("Glob result:")
    for i in ls:
        print(i)
    conn = sqlite_init(ls[0])
    base: pd.DataFrame = sqlite_exec(
        conn, f"SELECT * FROM TRACEROUTE_DATA")
    for db_file in ls[1:]:
        conn = sqlite_init(db_file)
        df: pd.DataFrame = sqlite_exec(
            conn, f"SELECT * FROM TRACEROUTE_DATA")
        base = pd.concat([base, df], axis=0)
    return base


def main():
    print("sqlite_load main")


if __name__ == "__main__":
    main()
