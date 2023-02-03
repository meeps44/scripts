from app.definitions.classdefinitions import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def cdf_plot(df: pd.DataFrame):
    """
    https://stackoverflow.com/questions/25577352/plotting-cdf-of-a-pandas-series-in-python
    """
    ser = pd.Series(np.random.normal(size=1000))
    ser.hist(cumulative=True, density=1, bins=100)
    plt.show()


def bar(df: pd.DataFrame):
    x = np.array(["A", "B", "C", "D"])
    y = np.array([3, 8, 1, 10])
    plt.bar(x, y)
    plt.show()


def scatter(df: pd.DataFrame):
    df = pd.read_csv('data.csv')
    df.plot(kind='scatter', x='Duration', y='Calories')
    plt.show()


def line(df: pd.DataFrame):
    y1 = np.array([3, 8, 1, 10])
    y2 = np.array([6, 2, 7, 11])
    plt.plot(y1)
    plt.plot(y2)
    plt.show()


def histogram(df: pd.Series):
    plt.hist(df)
    plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
