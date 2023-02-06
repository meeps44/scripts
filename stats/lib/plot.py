from lib.definitions.classdefinitions import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def cdf(sr: pd.Series):
    """
    https://stackoverflow.com/questions/25577352/plotting-cdf-of-a-pandas-series-in-python
    """
    sr.hist(cumulative=True, density=1, bins=100)
    plt.show()


def bar(sr: pd.Series):
    fig, ax = plt.subplots()
    bars = ax.bar([str(i) for i in sr.index], sr)
    ax.bar_label(bars)
    plt.show()


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
