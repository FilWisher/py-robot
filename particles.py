import time
import random
import math
import numpy as np
import sys

test_wall = (10,10,10,-10)

walls = [(0,0,0,10), (0,10,10,10), (10,10,10,0), (10,0,0,0)]

class Particles:
    def __init__(self, initial_location = (1,1,0), N=100):
        self.particles = []
        self.sigma = 1

        for i in xrange(0, N):
            self.particles.append((initial_location[0], initial_location[1], initial_location[2], 1.0/float(N)))

    def mean(self):
        xSum = 0
        ySum = 0
        thetaSum = 0
        numberOfTuples = len(self.particles)
        for particle in self.particles:
            x, y, theta, weight = particle
            xSum += x
            ySum += y
            thetaSum += theta

        return (xSum/numberOfTuples, ySum/numberOfTuples, thetaSum/numberOfTuples)

    def get_distance_to_closest_wall(self, particle, walls):
        minimum_distance = sys.maxint

        for wall in walls:
            distance_from_wall = self.calculate_distance_from_wall(particle, wall)
            if (self.check_particle_faces_wall(particle, wall, distance_from_wall)):
                # If we find a smaller distance set it
                if(minimum_distance > distance_from_wall):
                    minimum_distance = distance_from_wall

        return minimum_distance


    def calculate_distance_from_wall(self,particle, wall):
        x, y, theta, weight = particle
        theta_rad = np.deg2rad(theta)
        a_x, a_y, b_x, b_y = wall
        numerator = (b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)
        denominator = (b_y - a_y)*math.cos(theta_rad) - (b_x - a_x)*math.sin(theta_rad)
        if(denominator == 0):
            # print 'Warning denominator was zero in calculate_distance_from_wall'
            return -sys.maxint
        return numerator/denominator

    def in_range(self,x, x1, x2):
        x_min = x1 if (x1 < x2) else x2
        x_max = x1 if (x1 > x2) else x2

        if(x_min <= x <= x_max):
            return True
        else:
            return False

    def check_particle_faces_wall(self,particle,wall,m):
        """
        Note: edges cases like facing the corner of a wall return false
        """
        if(m < 0):
            return False
        x, y, theta, weight = particle
        a_x, a_y, b_x, b_y = wall
        x_intersection = x + m*(np.cos(np.deg2rad(theta)))
        y_intersection = x + m*(np.sin(np.deg2rad(theta)))
        if (self.in_range(x_intersection,a_x, b_x) and self.in_range(y_intersection,a_y, b_y)):
            return True
        else:
            return False

    def update_weights(self,walls,measurement):
        for i in xrange(len(self.particles)):
            difference = self.get_distance_to_closest_wall(self.particles[i], walls) - measurement
            likelihood = np.exp(-((difference)**2)/(2*self.sigma*self.sigma))
            x, y, theta, weight = self.particles[i]
            self.particles[i] = (x, y, theta, weight*likelihood)

    def normalize(self):
        sum = 0.0;
        for particle in self.particles:
            sum += particle[3]
        if(sum != 0):
            for i in xrange(len(self.particles)):
                x, y, theta, weight = self.particles[i]
                print type(weight), type(sum)
                self.particles[i] = (x, y, theta, weight / sum)
        else:
            print "you've really fucked up here"
            for i in xrange(len(self.particles)):
                x, y, theta, weight = self.particles[i]
                self.particles[i] = (x, y, theta, 1.0 / float(len(self.particles)) )

    def resample(self):
        """
        Resample N new particles with weight 1/N with distribution
        determined by weight of particles
        """
        samples = []
        particles_count = len(self.particles)
        for i in xrange(particles_count):
            r = random.random()
            sum = 0
            for particle in self.particles:
                x, y, theta, weight = particles
                sum += weight
                if (sum >= r):
                    samples.append((x, y, theta, 1.0/float(particles_count)))
                    break
        for i in xrange(0,particles_count):
            self.particles[i] = samples[i]

    def left(self, deg):
        for i in range(len(self.particles)):
            x,y,theta,weight = self.particles[i]
            g = random.gauss(0,0.2)
            self.particles[i] = (x, y, theta + deg + g, weight)

    def forwards(self, cm):
        #update particle position after moving cm distance
        for i in range(len(self.particles)):
                x,y,theta,weight = self.particles[i]
                e = random.gauss(0,1.6)
                f = random.gauss(0,1.6)

                self.particles[i] = ((x + (cm + e)*np.cos(np.deg2rad(theta))), (y + (cm + e)*np.sin(np.deg2rad(theta))), (theta + f), weight)

"""
    TESTING
"""
"""
test = Particles()
# print test.temp((0,0,45,0),(-10,10,10,10))

test.particles[0] = (5,5,0,0.01)

print test.get_distance_to_closest_wall(test.particles[0], walls)
test.left(45)
test.update_weights(walls, 7.07106)
print "UPDATED"
print test.particles
test.normalize()
print "NORMALIZED"
print test.particles

sum = 0
for particle in test.particles:
  sum += particle[3]
print "sum: ", sum

test.resample()
print "RESAMPLED"
print test.particles

print test.particles
print test.get_distance_to_closest_wall(test.particles[0], walls)
test.forwards(2)
print test.particles
print test.get_distance_to_closest_wall(test.particles[0], walls)
"""
