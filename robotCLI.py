import sys
import numpy as np

def planning(current_loc,goal):

    #need to translate our frame of reference
    x_c, y_c, theta_c = current_loc  #!!!!!make sure that theta_c is in degrees!
    x_g, y_g = goal

    dx = x_g - x_c
    dy = y_g - y_c

    d = np.sqrt(dx**2+dy**2)
    d_theta =  np.rad2deg(np.arctan2(dy,dx))-theta_c
    robot.left(d_theta)
    robot.forwards(d)

    return (x_g, y_g, d_theta+theta_c)

currentLoc = (0,0,0)

while(True):
    print 'I am at ', currentLoc, ' where would you like me to go? (Format: x y)'
    array = map(int,(sys.stdin.readline()).split(' '))
    if(len(array) != 2):
        print 'Invalid position ', array
    print 'Setting course for ', array
    currentLoc = planning(currentLoc,array)
    print 'Arrived at ', currentLoc
