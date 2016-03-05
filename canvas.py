#!/usr/bin/env python

# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math
import numpy as np
#import robot
import particles as ps

def roundTuple(t):
    return tuple(map(lambda x: round (x,3), t))

# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size;
        self.scale       = self.canvas_size/(map_size+2*self.margin);

    def drawLine(self,line):
        x1 = self.__screenX(line[0]);
        y1 = self.__screenY(line[1]);
        x2 = self.__screenX(line[2]);
        y2 = self.__screenY(line[3]);
        print "drawLine:" + str((x1,y1,x2,y2))

    def drawParticles(self,data):
        display = [(self.__screenX(d[0]),self.__screenY(d[1])) + d[2:] for d in data];
        print "drawParticles:" + str(display);

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
    def __init__(self,canvas):
        self.walls = [];
        self.canvas = canvas

    def add_wall(self,wall):
        self.walls.append(wall);

    def clear(self):
        self.walls = [];

    def draw(self):
        for wall in self.walls:
            self.canvas.drawLine(wall);

    def getWalls(self):
        return self.walls

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


canvas = Canvas();    # global canvas we are going to draw on
theMap = Map(canvas);
# Definitions of walls
theMap.add_wall((0,0,0,168));        # a
theMap.add_wall((0,168,84,168));     # b
theMap.add_wall((84,126,84,210));    # c
theMap.add_wall((84,210,168,210));   # d
theMap.add_wall((168,210,168,84));   # e
theMap.add_wall((168,84,210,84));    # f
theMap.add_wall((210,84,210,0));     # g
theMap.add_wall((210,0,0,0));        # h
theMap.draw();
walls = theMap.getWalls()

class WaypointNavigation:
    def __init__(self,useRobot,waypoints,initialWaypoint,noParticles,startAngle=0):
        self.useRobot = useRobot
        self.waypoints = waypoints
        x0, y0 = waypoints[initialWaypoint]
        self.initial_location = (x0,y0,startAngle)
        self.particles = ps.Particles(self.initial_location,noParticles)
        self.initialWaypoint = initialWaypoint

    def navigate(self):
        current_location = self.initial_location

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
                robot.left(angle)
            print ' moving forwards ', round(distance,1)
            robot.forwards(distance)
        if(abs(angle) > 2.0):
            self.particles.left(angle)
        self.particles.forwards(distance)


        canvas.drawParticles(self.particles.data)
        return self.particles.mean()
