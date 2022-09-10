import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def create_plot(dataframe):
    data = dataframe[['Flow label', 'Source IP']].head(10)
    data.plot()
    plt.show()


def load_single_csv(filename):
    # Load data into DataFrame
    df: pd.DataFrame = pd.read_csv(
        filename, sep=', ', parse_dates=['Timestamp'])
    return df


def load_multiple_csv(path):
    try:
        all_files = glob.glob(os.path.join(path, "*.csv"))
        df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        return df
    except FileNotFoundError:
        print("Error: No such file or directory")
        exit(1)
    except NotADirectoryError:
        print("Error: Not a directory")
        print("Please use the --file option to compare single files. Use the -h argument for more info.")
        exit(1)


def latex_convert(dataframe):
    with open('table.tex', 'w') as file:
        file.write(dataframe.to_latex())


def print_stats(dataframe):
    # Print all rows
    print(dataframe)
    # Print top rows
    print(dataframe.head())
    # Print column
    print(dataframe['Flow label'].head())
    # Print multiple columns
    print(dataframe[['Flow label', 'Source IP']].head())
    # Print data types of each column
    print(dataframe.dtypes)


def main():
    filename = "test_data.csv"
    #path = "/home/erlend/git/scripts/september/csv"
    #traceroute_stats = load_multiple_csv(path)
    traceroute_stats = load_single_csv(filename)
    print_stats(traceroute_stats)
    create_plot(traceroute_stats)


if __name__ == "__main__":
    main()
