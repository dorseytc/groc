import numpy as np
import matplotlib.pyplot as plt
x=range(1,6)
if True:
  y1=[1,4,6,8,9]
  y2=[2,2,7,18,9]
  y3=[2,8,6,8,2]
  plt.stackplot(x, y1, y2, y3, labels=['A', 'B', 'C'])
  plt.legend(loc='upper left')
  plt.show()
print("done")
