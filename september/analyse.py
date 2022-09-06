import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_plot(traceroute_stats):
    data = traceroute_stats[['Flow label', 'Source IP']].head(10)
    data.plot()
    plt.show()


def load_csv():
    # Load data into DataFrame
    traceroute_stats = pd.read_csv(
        'test_data.csv', sep=',', parse_dates=['Timestamp'])
    # Print all rows
    print(traceroute_stats)
    # Print top rows
    print(traceroute_stats.head())
    # Print column
    print(traceroute_stats['Flow label'].head())
    # Print multiple columns
    print(traceroute_stats[['Flow label', 'Source IP']].head())
    # Print data types of each column
    print(traceroute_stats.dtypes)


def main():
    load_csv()
    create_plot()


if __name__ == "__main__":
    main()