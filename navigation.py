#!/usr/bin/env python

# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math
import numpy as np
import particles as ps
from canvas import *

def roundTuple(t):
    return tuple(map(lambda x: round (x,3), t))

# CW 3 WAYPOINTS
waypoints_cw3 = []
waypoints_cw3.append((180, 30))
waypoints_cw3.append((180, 54))
waypoints_cw3.append((138, 54))
waypoints_cw3.append((138, 168))
waypoints_cw3.append((114, 168))
waypoints_cw3.append((114, 84))
waypoints_cw3.append((84, 84))
waypoints_cw3.append((84, 30))
# CW 4 WAYPOINTS
waypoints_cw4 = []
waypoints_cw4.append((84, 30))
waypoints_cw4.append((180, 30))
waypoints_cw4.append((180, 54))
waypoints_cw4.append((138, 54))
waypoints_cw4.append((138, 168))

class WaypointNavigation:
    def __init__(self,waypoints,initialLocation,noParticles,startAngle=0,robot=None):
        self.useRobot = (robot != None)
        self.robot = robot
        self.waypoints = waypoints
        x0, y0 = initialLocation
        self.initial_location = (x0,y0,startAngle)
        self.particles = ps.Particles(self.initial_location,noParticles)

    # Set the particle angles such that the mean is in the center of a range
    def init_angular_uncertainity(self,(min,max)):
        N = len(self.particles.data)
        step = float(max-min)/float(N)
        for i in xrange(N):
            x, y, theta = self.particles.data[i]
            self.particles.data[i] = (x, y, min + step*i)


    def navigate(self):
        current_location = self.particles.mean()

        for i,waypoint in enumerate(self.waypoints):
            print '\n\nNavigation', i+1, 'from', roundTuple(current_location),'to',roundTuple(waypoint)
            current_location = self.move_in_steps(current_location,waypoint)

    def calculate_movement(self,current, destination):
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

    def move_in_steps(self,current_loc,destination,step_size=10):

        def vector_length(x,y):
            return np.sqrt(x**2 + y**2)

        x0, y0, theta0 = current_loc
        x1, y1 = destination

        dx = x1 - x0
        dy = y1 - y0

        # normalise dx, dy to get a unit vector
        norm = np.sqrt(dx**2 + dy**2)
        if norm > 0:
          dx /= norm
          dy /= norm
        else:
          dx = 0.0
          dy = 0.0

        print 'Unit vector : ', roundTuple((dx,dy))

        while True:
            new_x = x0 + dx*step_size
            new_y = y0 + dy*step_size
            if( vector_length(dx*step_size,dy*step_size) < vector_length(x1-x0,y1-y0)  ):
                newLocation = self.move((x0,y0,theta0),(new_x,new_y),True)
                x0, y0, theta0 = newLocation
            else:
                return self.move((x0,y0,theta0), destination,True)

    def move(self,current_loc, destination,mcl=False):

        canvas.drawParticles(self.particles.data)

        if self.useRobot:
            measurement = self.robot.getSensorMeasurement()
        else:
            measurement = self.particles.getFakeSensorMeasurement(walls,canvas=canvas)
        print "measurement: ", measurement

        if mcl:
            self.particles.do_mcl(walls, measurement)

        print "mean: ", roundTuple(self.particles.mean()), " wanted: ", roundTuple(destination)

        distance, angle = self.calculate_movement(current_loc, destination)
        if self.useRobot:
            if(abs(angle) > 2.0):
                print 'Turning ', round(angle,1),
                self.robot.left(angle)
            print ' moving forwards ', round(distance,1)
            self.robot.forwards(distance)
        if(abs(angle) > 2.0):
            self.particles.left(angle)
        self.particles.forwards(distance)


        canvas.drawParticles(self.particles.data)
        return self.particles.mean()
