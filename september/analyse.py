import pandas as pd
import numpy as np


def create_plot():
    # Load data into DataFrame
    traceroute_stats = pd.read_csv('test_data.csv', sep=',')
    print(traceroute_stats)
    print(traceroute_stats.head())


def main():
    pass


if __name__ == "__main__":
    main()
