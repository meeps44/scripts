import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def create_plot(dataframe):
    data = dataframe[['Flow label', 'Source IP']].head(10)
    data.plot()
    plt.show()


def load_single_csv(filename) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(
        filename, sep=', ', parse_dates=['Timestamp'])
    return df


def load_multiple_csv(path) -> pd.DataFrame:
    try:
        all_files = glob.glob(os.path.join(path, "*.csv"))
        df: pd.DataFrame = pd.concat((pd.read_csv(f, low_memory=False)
                                     for f in all_files), ignore_index=True)
        return df
    except FileNotFoundError:
        print("Error: No such file or directory")
        exit(1)
    except NotADirectoryError:
        print("Error: Not a directory")
        print("Please use the --file option to compare single files. \
            Use the -h argument for more info.")
        exit(1)


def export_to_latex(dataframe):
    with open('table.tex', 'w') as file:
        file.write(dataframe.to_latex())


def print_stats(dataframe):
    # Print all rows
    # print(dataframe)
    # Print top rows
    # print(dataframe.head())
    # Print column
    # print(dataframe['Flow label'].head())
    # Print multiple columns
    # print(dataframe[['Flow label', 'Source IP']].head())
    # Print data types of each column
    # print(dataframe.dtypes)
    # Select row by index
    print(dataframe.iloc[[413, 414]])
    # Select row by value and print whole row
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(dataframe.loc[dataframe['Destination IP']
              == "2001:410:112:32::1"])


def main():
    # filename = "/home/erlend/csv-storage/csv-storage/ubuntu-lon1-0-2022-09-12T20_27_07Z.csv"
    # df = load_single_csv(filename)
    # path = "/home/erlend/git/scripts/september/csv"
    path = "/home/erlend/git/scripts/september/tarballs/unzip"
    df = load_multiple_csv(path)
    print_stats(df)
    # create_plot(traceroute_stats)
    # export_to_latex(traceroute_stats)


if __name__ == "__main__":
    main()
