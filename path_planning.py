

import numpy as np



def navigatetoWaypoint(X,Y):


    #assuming robot is at (0,0,0) 
    
    #xnew = cos(theta)*d
    #ynew = sin(theta)*d

    d = np.sqrt(X*X + Y*Y)
    sin_theta = Y/d
    cos_theta = X/d

    #theta is in radians
    theta_rad = acos(cos_theta)
    
    #turn theta into degrees
    theta_deg = theta_rad * 360 / 2* np.pi

    #call function that rotates robot by theta_deg degrees
    

    #call function to move robot straight for d cm



def path_planning(current_loc, goal):

    #need to translate our frame of reference
    x_c, y_c, theta_c = current_loc  #!!!!!make sure that theta_c is in degrees!
    x_g, y_g = goal


    #calculate angle of goal point with respect to real frame
    sin_theta = y_g/d
    cos_theta = x_g/d

    #theta is in radians
    theta_rad = acos(cos_theta)
    
    #turn theta into degrees
    theta_deg = theta_rad * 360 / 2* np.pi  
   
    
    
    #subtract the angle robot is facing  with respect to real frame from angle of goal point
    #to obtain abgle the robot needs to turn to
    #if this angle is negative, robot has to turn this amount right
    #if angle is positive, robot has to turn this amount left
    theta_to_move = theta_deg - theta_c

    if theta_to_move < 0:
        #turn right amount theta_to_move

    else: 
        #turn left amount theta_to_move
    
    #xnew = cos(theta)*d
    #ynew = sin(theta)*d
    X = abs(x_c - x_g)
    Y = abs(y_c - y_g)
    d = np.sqrt(X*X + Y*Y)

    
    #after turned into correct direction, move d cm forward
    
    


    
