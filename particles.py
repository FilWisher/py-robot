import time
import random
import math
import numpy as np
import sys


#using SIGMAX and SIGMAY = 0.9
#using straight rotational sigma of 0.2
#using pure rotational sigma of 0.2

def unit_vector(deg):
  """
  Returns unit vector in form (x, y) from angle in degrees
  """
  rad = np.deg2rad(deg)
  return (np.cos(rad), np.sin(rad))

def mean_angle(particles):
  """
  Averages angles via unit vector conversions to circumvent
  weirdness of averageing 360 with 0
  """
  angles = map(lambda x: x[2], particles)
  sum = [0, 0]
  uvectors = map(unit_vector, angles)
  for uvector in uvectors:
    sum[0] += uvector[0]
    sum[1] += uvector[1]
  average = [float(sum[0])/float(len(uvectors)), float(sum[1])/float(len(uvectors))]
  return np.rad2deg(np.arctan2(average[1], average[0]))


class Particles:
    def __init__(self, initial_location = (1,1,0), N=100):
        self.data    = []
        self.weights      = []
        self.safe_to_update = []
        self.nearest_wall = []
        self.distance_to_nearest_wall = []
        self.sigma = 1.0

        for i in xrange(0, N):
            self.data.append((initial_location[0], initial_location[1], initial_location[2]))
            self.weights.append(1.0/float(N))
            self.safe_to_update.append(True)
            self.nearest_wall.append(-1)

    #calculates the mean values for x,y and theta of the particle cloud
    def mean(self):
        xSum = 0
        ySum = 0
        thetaSum = 0
        numberOfTuples = len(self.data)
        for particle in self.data:
            x, y, theta = particle
            xSum += x
            ySum += y
            thetaSum += theta

        return (xSum/numberOfTuples, ySum/numberOfTuples, mean_angle(self.data))

    def update_nearest_walls(self,walls):
        self.nearest_wall = []
        self.distance_to_nearest_wall = []
        for i in xrange(len(self.data)):
            wall_index, distance = self.get_distance_to_nearest_wall(self.data[i], walls)
            self.nearest_wall.append(wall_index)
            self.distance_to_nearest_wall.append(distance)

    def get_distance_to_nearest_wall(self, particle, walls):
        nearest_wall_distance = 2000
        nearest_wall_index = -1
        for i in xrange(len(walls)):
            distance_from_wall = self.distance_from_wall(particle, walls[i])
            ok = self.check_particle_faces_wall(particle, walls[i], distance_from_wall)
            if (ok):
                # If we find a smaller distance set it
                if(nearest_wall_distance > distance_from_wall):
                    nearest_wall_distance = distance_from_wall
                    nearest_wall_index = i
        return ( nearest_wall_index, nearest_wall_distance )


    def orthogonal_distance_from_wall(self,particle,wall):
        # Used https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        x0, y0, theta = particle
        theta_rad = np.deg2rad(theta)
        x1, y1, x2, y2 = wall
        numerator = np.abs( (y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1 )
        denominator = np.sqrt((y2-y1)**2 + (x2 - x1)**2)
        if denominator == 0:
            print 'Warning! Found wall of zero length!'
            return -1
        return numerator/denominator

    def check_measurement_is_safe(self,particle_index,walls):
        nearest_wall_index = self.nearest_wall[particle_index]
        if nearest_wall_index == -1:
                return False
        distance_to_wall = self.distance_to_nearest_wall[particle_index]
        short_distance_to_wall = self.orthogonal_distance_from_wall(self.data[particle_index], walls[nearest_wall_index])
        angle_with_wall = np.arccos(short_distance_to_wall/distance_to_wall)
        #error measurements indicated that at an angle of 40 degrees from point to walls
        #measurements become unreliable. Used 180 - 90 - 40 = 50 degrees:
        if(np.rad2deg(angle_with_wall) > 40):
            return False
        else:
            return True

    def distance_from_wall(self,particle, wall):
        x, y, theta = particle
        theta_rad = np.deg2rad(theta)
        a_x, a_y, b_x, b_y = wall
        numerator = (b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)
        denominator = (b_y - a_y)*math.cos(theta_rad) - (b_x - a_x)*math.sin(theta_rad)
        if(denominator == 0):
            # print 'Warning denominator was zero in distance_from_wall'
            return -sys.maxint
        return numerator/denominator

    def in_range(self,x, a, b):
        # tolerance to avoid strange edge cases
        ds = 1e-10
        ok1 = a - ds <= x <= b + ds
        ok2 = a + ds >= x >= b - ds
        if(ok1 or ok2):
            return True
        else:
            return False

    def check_particle_faces_wall(self,particle,wall,m):
        """
        Note: edges cases like facing the corner of a wall return false
        """
        if(m < 0):
            return False
        x, y, theta = particle
        a_x, a_y, b_x, b_y = wall
        x_intersection = x + m*(np.cos(np.deg2rad(theta)))
        y_intersection = y + m*(np.sin(np.deg2rad(theta)))
        if (self.in_range(x_intersection,a_x, b_x) and self.in_range(y_intersection,a_y, b_y)):
            return True
        else:
            return False

    def update_is_safe(self, walls):
        self.safe_to_update = []
        trues = 0
        for i in xrange(len(self.data)):
            self.safe_to_update.append(self.check_measurement_is_safe(i, walls))
        for i in xrange(len(self.safe_to_update)):
            if self.safe_to_update[i]:
                trues += 1
        if trues > len(self.data)/2:
            print 'ITS SAFE: ', trues, '%'
            return True
        else:
            print 'NOT SAFE', trues, '%'
            return False


    def update_weights(self,walls,measurement):
        for i in xrange(len(self.data)):
            #make sure that the distance_to_nearest wall is not 2000 (the default value)
            if self.distance_to_nearest_wall[i] != 2000:
                difference = self.distance_to_nearest_wall[i] - measurement
                arg = -((float(difference))**2)/(2*self.sigma**2)
                likelihood = np.exp(arg)
                self.weights[i] = self.weights[i]*likelihood

    def do_mcl(self,walls,measurement):
        #for each particle, finds the nearest wall and the distance to it.
        self.update_nearest_walls(walls)
        #determine if it is safe to update
        if self.update_is_safe(walls):
            self.update_weights(walls, measurement)
            self.normalize()
            self.resample()


    def normalize(self):
        sum = 0.0;
        for weight in self.weights:
            sum += weight
        if(sum != 0):
            for i in xrange(len(self.data)):
                self.weights[i] = self.weights[i]/sum
        else:
            print "Warning! Particle weights got really small!"
            for i in xrange(len(self.data)):
                self.weights[i] = 1.0/float(len(self.data))

    def resample(self):
        """
        Resample N new particles with weight 1/N with distribution
        determined by weight of particles
        """
        new_particles = []
        particles_count = len(self.data)
        for i in xrange(particles_count):
            r = random.random()
            sum = 0
            for i in xrange(len(self.weights)):
                sum += self.weights[i]
                if (sum >= r):
                    new_particles.append(self.data[i])
                    break

        for i in xrange(0,particles_count):
            self.weights[i] = 1.0/float(particles_count)

        self.data = new_particles

    def left(self, deg):
        for i in range(len(self.data)):
            x,y,theta = self.data[i]
            g = random.gauss(0,0.4)
            self.data[i] = (x, y, theta + deg + g)

    def forwards(self, cm):
        #update particle position after moving cm distance
        for i in range(len(self.data)):
                x,y,theta = self.data[i]
                e = random.gauss(0,2.0)
                f = random.gauss(0,2.0)

                self.data[i] = ((x + (cm + e)*np.cos(np.deg2rad(theta))), (y + (cm + e)*np.sin(np.deg2rad(theta))), (theta + f))

    def getFakeSensorMeasurement(self,walls,angle=0.0,canvas=None):
        x0, y0, theta0 = self.mean()
        newPos = (x0, y0, theta0 + angle)
        i, d = self.get_distance_to_nearest_wall(newPos,walls)
        if(canvas != None):
            rads = np.deg2rad(theta0 + angle)
            canvas.drawLine((x0,y0,x0+d*np.cos(rads),y0+d*np.sin(rads)))
        return d+random.gauss(0.0,0.5)
