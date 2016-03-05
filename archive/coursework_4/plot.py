import numpy as np
import matplotlib.pyplot as plt

a = np.loadtxt('angle_vs_distance.dat')
plt.plot(a[:,0],a[:,1])
plt.xlabel('angle')
plt.ylabel('distance')
plt.show()
