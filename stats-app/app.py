from statistics.filter import *
from statistics.plot import *


def main():
    stats = TracerouteStatistics()
    source_flow_labels = [0, 255, 1048575]
    # Get all databases in directory.
    ls: list = glob.glob(
        "/home/erlhap/test/python/paris-traceroute-filter/data/*.db")
    for db_file in ls:
        conn = sqlite_init(db_file)
        unique_start_times = get_unique_start_times(conn)
        for time in unique_start_times:
            for fl in source_flow_labels:
                df = sqlite_exec(
                    conn, f"SELECT PATH_HASH FROM TRACEROUTE_DATA WHERE START_TIME={time} AND SOURCE_FLOW_LABEL={fl}")
        print(df)


if __name__ == "__main__":
    main()
