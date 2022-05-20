import numpy as np
import matplotlib.pyplot as plt

filepath = "C:\\Users\\Erlend\\Documents\\Programming\\Python programming\\data.txt"
with open(filepath, "r") as file:
    data = file.readlines()
    data = list(map(int, data)) # Convert input data from str to int
    N = len(data)

X = np.sort(data)
Y = np.array(range(N))/float(N)

plt.plot(X, Y, label="CDF")
plt.xticks(np.arange(min(data), max(data)+1, 1.0))
plt.xlabel("Hop number")
plt.ylabel("Probability that the amount of hop numbers is less than H")
plt.legend()
plt.show()
