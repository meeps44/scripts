from dataclasses import dataclass
from sqlite3 import connect
import pandas as pd


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0

def number_of_equal_paths(flowlabel: int):
    pass

def hop_where_path_diverged(flowlabel: int):
    pass

def main():
    pass

if __name__ == "__main__":
    main()
