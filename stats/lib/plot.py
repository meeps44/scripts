from lib.definitions.classdefinitions import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def cdf(data: pd.Series):
    """
    https://stackoverflow.com/questions/25577352/plotting-cdf-of-a-pandas-series-in-python
    https://www.tutorialspoint.com/how-to-plot-cdf-in-matplotlib-in-python
    sr.hist(cumulative=True, density=1, bins=100)
    """
    count, bins_count = np.histogram(data, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.legend()
    plt.show()


def bar(sr: pd.Series):
    fig, ax = plt.subplots()
    bars = ax.bar([str(i) for i in sr.index], sr)
    ax.bar_label(bars)


def scatter(sr: pd.Series):
    sr.plot(kind='scatter', x='Duration', y='Calories')
    plt.show()


def line(sr: pd.Series):
    plt.plot(sr)
    plt.show()


def histogram(sr: pd.Series):
    plt.hist(sr)
    plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
