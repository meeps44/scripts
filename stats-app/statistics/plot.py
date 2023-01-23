import pandas as pd
import matplotlib.pyplot as plt


def plot():
    df = pd.read_csv('data.csv')
    df.plot(kind='scatter', x='Duration', y='Calories')
    plt.show()


def main():
    plot()


if __name__ == "__main__":
    main()
