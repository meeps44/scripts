from stats.definitions.classdefinitions import *
from sqlite3 import connect
import pandas as pd


def compare_path_hash(df: pd.DataFrame, flowlabel: int, start_time: int):
    """
    Compare the path hash of all paths in the dataset with the same START_TIME and SOURCE_FLOW_LABEL.
    Return the number of instances where the path stayed the same.
    """
    indices = list()
    src_fl: str = df['SOURCE_FLOW_LABEL']
    for row_idx in df.index:
        hrfl: str = df['HOP_RETURNED_FLOW_LABELS'][row_idx]
        flow_labels: list = hrfl.split(" ")
        for val in flow_labels:
            if src_fl != val:
                indices.append(row_idx)
                break
    return indices


def main():
    pass


if __name__ == "__main__":
    main()
