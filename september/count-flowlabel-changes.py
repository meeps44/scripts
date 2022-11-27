import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Iterates through each row in a csv, and counts
# the number of instances the returned flow label differs
# from the source flow label.


def load_single_csv(filename) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(
        filename, sep=', ', parse_dates=['Timestamp'])
    return df


def main():
    # filename = "/home/erlend/csv-storage/csv-storage/ubuntu-lon1-0-2022-09-12T20_27_07Z.csv"
    filename = "/home/erlend/git/scripts/september/tarballs/unzip/ubuntu-ams3-0-2022-09-26T11_53_32Z.csv"
    df = load_single_csv(filename)


if __name__ == "__main__":
    main()
