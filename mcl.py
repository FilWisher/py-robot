import numpy as np
import robot

## INITIALIZE:
# create particles
particles_count = 100
particles = [(100, 100, 0) for i in range(particlesCount)]
# initialize current loc
current_location = (0, 0, 0)

## MOVE:
# 1. accept movement and predict motion for particles
# 2. get sonar measurement
# 3. calculate new weights
# 4. normalise 
# 5. resample 
# 6. current location = mean(particles)

def calculate_movement(current, destination):
    current_x, current_y, current_theta = current
    x, y = destination
    dx = x - current_x
    dy = y - current_y
    
    d = np.sqrt(dx**2+dy**2)
    d_theta = np.rad2deg(np.arctan2(dy,dx))-current_theta)
    if(d_theta > 180):
	d_theta -= 360
    elif(d_theta < -180):
	d_theta += 360
        
    return d, d_theta
    

def move(x, y):
 
    # TODO: when do we take the mean of particles?
    
    d, d_theta = calculate_movement(current_location, (x,y))
    robot.left(d_theta)
    robot.forwards(d)
       
    particles.left(d_theta)
    particles.forwards(d)
    
    current_location = particles.mean() 
    # 1. 
    # calculate theta
    # calculate distance
    # move robot
    # move particles
