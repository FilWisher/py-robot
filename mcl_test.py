import random
import numpy as np
import time
import robot
import particles as p

#helper functions
def drawWalls():
    for wall in walls:
        print "drawLine:" + str(wall)

def moveParticles(cm):
    particles.forwards(cm)
    saveParticles()

def turnParticles(deg):
    particles.left(deg)
    saveParticles()

def printParticles():
    saveParticles()
    print "drawParticles:" + str(particleHistory)

def saveParticles():
    for p in particles.particles:
        particleHistory.append(p)

def vector_length(x,y):
     return np.sqrt(x**2 + y**2)

#function which uses the code from our waypoint navigation function path_planning
def calculate_movement(current, destination):
    current_x, current_y, current_theta = current
    x, y = destination
    dx = x - current_x
    dy = y - current_y

    d = np.sqrt(dx**2+dy**2)
    d_theta = np.rad2deg(np.arctan2(dy,dx))-current_theta
    if(d_theta > 180):
        d_theta -= 360
    elif(d_theta < -180):
        d_theta += 360

    return d, d_theta

#function which moves the robot in steps
def move_in_steps(current_loc,destination,step_size=20):

    x0, y0, theta0 = current_loc
    x1, y1 = destination

    dx = x1 - x0
    dy = y1 - y0

    # normalise dx, dy to get a unit vector
    norm = np.sqrt(dx**2 + dy**2)
    dx /= norm
    dy /= norm

    while True:
        print "drawParticles:" + str(particles.particles)
        new_x = x0 + dx*step_size
        new_y = y0 + dy*step_size
        if( vector_length(new_x,new_y) < vector_length(x1,y1)  ):
            move((x0,y0,theta0),(new_x,new_y))
            x0 = new_x
            y0 = new_y
        else:
            return move((x0,y0,theta0), destination)

#function which moves the robot from current_loc to destination using waypoint navigation
def move(current_loc, destination):
    distance, angle = calculate_movement(current_loc, destination)
    # robot.left(angle)
    # robot.forwards(distance)
    particles.left(angle)
    particles.forwards(distance)

    #if using mcl, get the measurement and use the mcl algorithm
    #measurement = robot.getSensorMeasurement()
    #print "measurement: ", measurement
    #particles.do_mcl(walls, measurement)
    #print "mean: ", particles.mean(), " wanted: ", destination

    #return the new mean of the particles if using mcl
    #return particles.mean()

    #otherwise, return the destination, if not using mcl correction
    return destination

#function which makes the robot go to a number of waypoints
def journey(waypoints):
    #save the mean of the particle cloud in current location
    current = particles.mean()
    for waypoint in waypoints:
        #move the robot to waypoint in steps.
        #Note that if using mcl, move_in_steps will return the new particle mean calculated after mcl.
        #If not using mcl, current will simply be the waypoint, as we assume we arrived at waypoint,
        old = current
        current = move_in_steps(old, waypoint)
        #print "drawLine:" + str((old[0], old[1], current[0], current[1]))

    # TODO: draw line from old loc to current each time
    # TODO: keep track of history of particles


#function which makes the robot adjust its position using mcl. It returns true only if within 10 cm of waypoint
def update_position(current_loc, waypoint):
    #move the robot from location it got to to the corrected position after sonar measurement
    distance, angle = calculate_movement(current_loc, waypoint)
    robot.left(angle)
    robot.forwards(distance)

    #get the new particle mean
    mean = particles.mean()

    #check if close enough to waypoint

    x_mean, y_mean, alpha_mean = mean
    x_way, y_way = way
    dx = x_mean - x_way
    dy = y_mean - y_way
    diff = vector_length(dx,dy)
    
    if diff <= 10:
        return True
    else:
        return False



#initialise particles
particles = p.Particles((84,30,0), 100)

numberOfParticles = 100

particleHistory = []

# ASSESSMENT STUFF
#walls = [(0,0,0,168), (0,168,84,168), (84,126,84,210), (84,210,168,210), (168,210,168,84), (168,84,210,84), (210,84,210,0)]
#waypoints = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]

# TEST WORLD
#walls = [(130,50,130,-50)]
#waypoints = [(100,50)]
print "drawParticles:" + str(particles.particles)
drawWalls()
journey(waypoints)

# current_loc = particles.mean()
# print "drawParticles:" + str(particles.particles)
#
# x, y, theta = current_loc
# current_loc = move(current_loc,(x+30,y))
# print "drawParticles:" + str(particles.particles)
#
# x, y, theta = current_loc
# current_loc = move(current_loc,(x+30,y))
# print "drawParticles:" + str(particles.particles)
