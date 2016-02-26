import numpy as np
import matplotlib.pyplot as plt

a = np.loadtxt('data_garbage_meas.dat')
plt.plot(a[:,0],a[:,1])
plt.title('Looking for garbage values from sensors')
plt.xlabel('angle (degrees)')
plt.ylabel('distance (cm)')
plt.show()
