import numpy as np

test_angles = [360, 358, 2, 0]

def mean_angle(angles):
  sum = 0;
  for angle in angles:
    sum += angle
  return (float(sum) / len(angles))


def unit_vector(deg):
  """
  Returns unit vector in form (x, y) from angle in degrees
  """
  rad = np.deg2rad(deg)
  return (np.cos(rad), np.sin(rad))
  
def mean_angle2(angles):
  return map(unit_vector, angles)
  
 
print mean_angle2(test_angles)
print mean_angle(test_angles)
