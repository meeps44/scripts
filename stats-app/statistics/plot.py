import pandas as pd
import matplotlib.pyplot as plt


def plot():
    df = pd.read_csv('data.csv')
    df.plot(kind='scatter', x='Duration', y='Calories')
    plt.show()


def cdf_plot(df: pd.DataFrame):
    pass

def bar_plot(df: pd.DataFrame):
    pass

def scatter_plot(df: pd.DataFrame):
    pass

def line_plot(df: pd.DataFrame):
    pass

def histogram_plot(df: pd.DataFrame):
    pass

def main():
    plot()


if __name__ == "__main__":
    main()
