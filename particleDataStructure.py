#!/usr/bin/env python

# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math
import numpy as np

# Functions to generate some dummy particles data:
def calcX():
    return random.gauss(80,3) + 70*(math.sin(t)); # in cm

def calcY():
    return random.gauss(70,3) + 60*(math.sin(2*t)); # in cm

def calcW():
    return random.random();

def calcTheta():
    return random.randint(0,360);

# A Canvas class for drawing a map and particles:
# 	- it takes care of a proper scaling and coordinate transformation between
#	  the map frame of reference (in cm) and the display (in pixels)
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
    def __init__(self):
        self.walls = [];

    def add_wall(self,wall):
        self.walls.append(wall);

    def clear(self):
        self.walls = [];

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall);

# Simple Particles set
class Particles:
    def __init__(self):
        self.n = 10;
        self.data = [];

    def update(self):
        self.data = [(calcX(), calcY(), calcTheta(), calcW()) for i in range(self.n)];

    def draw(self):
        canvas.drawParticles(self.data);

canvas = Canvas();	# global canvas we are going to draw on

mymap = Map();
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
mymap.add_wall((0,0,0,168));        # a
mymap.add_wall((0,168,84,168));     # b
mymap.add_wall((84,126,84,210));    # c
mymap.add_wall((84,210,168,210));   # d
mymap.add_wall((168,210,168,84));   # e
mymap.add_wall((168,84,210,84));    # f
mymap.add_wall((210,84,210,0));     # g
sigma = 2
mymap.add_wall((210,0,0,0));        # h
mymap.draw();

particles = Particles();

def calculate_distance_from_wall(particle, wall):
    weight, x, y, theta = particle
    theta_rad = np.deg2rad(theta)
    a_x, a_y, b_x, b_y = wall
    numerator = (b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)
    denominator = (b_y - a_y)*math.cos(theta_rad) - (b_x - a_x)*math.sin(theta_rad)
    return numerator/denominator

test_particles = [(0.5,0,0,0), (0.5,1,1,0)]
test_measurement = 8
test_wall = (10,-10,10,10)
for p in test_particles:
    difference = calculate_distance_from_wall(p,test_wall)-test_measurement
    print np.exp(-((difference)**2)/(2*sigma*sigma))

def update_weights(particles):
    for i in xrange(len(particles)):
        difference = calculate_distance_from_wall(p,test_wall)-test_measurement
        likelihood = np.exp(-((difference)**2)/(2*sigma*sigma))
        weight, x, y, theta = particles[i]
        particles[i] = (weight*likelihood, x, y, theta)

def normalize_weights(particles):
    sum = 0;
    for particle in particles:
        sum += particle[0]
    for i in xrange(len(particles)):
        weight, x, y, theta = particles[i]
        particles[i] = (weight / sum, x, y, theta)

def resample(particles, N):
    samples = []
    for i in xrange(N):
        r = random.random()
        sum = 0;
        for j in xrange(len(particles)):
            sum += particles[j]
            if (sum > r):
                samples[j] = particles[j]
    for i in xrange(len(samples)):
        particles[i] = samples[i];




def resample(particles, N):
    """
    Resample N new particles with weight 1/N with distribution
    determined by weight of particles
    """
    samples = []
    for i in xrange(N):
        r = random.random()
        sum = 0
        for j in xrange(len(particles)):
            weight, x, y, theta = particles[i]
            sum += weight
            if (sum > r):
                samples[i] = (1/N, x, y, theta)
    for i in xrange(len(samples)):
        particles[i] = samples[i]
                

# t = 0;
# while True:
#     particles.update();
#     particles.draw();
#     t += 0.05;
#     time.sleep(0.05);
