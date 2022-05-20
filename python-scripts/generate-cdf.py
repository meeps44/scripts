import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#%matplotlib inline

filepath = "C:\\Users\\Erlend\\Documents\\Programming\\Python programming\\data.txt"
with open(filepath, "r") as file:
    data = file.readlines()
    N = len(data)
    arr = np.array(data)

X2 = np.sort(data)
F2 = np.array(range(N))/float(N)

plt.plot(X2, F2, label="CDF")
plt.legend()
plt.show()
