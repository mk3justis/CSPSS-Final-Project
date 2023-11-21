import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 4*np.pi, 0.1)
y = np.sin(4*x)

plt.plot(x,y,color='red')
plt.show()

# Credit to:
# https://www.geeksforgeeks.org/plotting-sine-and-cosine-graph-using-matloplib-in-python/