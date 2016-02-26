import time
import random
import math
import numpy as np
import sys

#test_wall = (10,10,10,-10)
#walls = [(0,0,0,10), (0,10,10,10), (10,10,10,0), (10,0,0,0)]


class Particles:
    def __init__(self, initial_location = (1,1,0), N=100):
        self.particles    = []
        self.weights      = []
        self.safe_to_update = []
        self.nearest_wall = []
        self.distance_to_nearest_wall = []
        self.sigma = 1

        for i in xrange(0, N):
            self.particles.append((initial_location[0], initial_location[1], initial_location[2]))
            self.weights.append(1.0/float(N))
            self.safe_to_update.append(True)
            self.nearest_wall.append(-1)

    #calculates the mean values for x,y and theta of the particle cloud
    def mean(self):
        xSum = 0
        ySum = 0
        thetaSum = 0
        numberOfTuples = len(self.particles)
        for particle in self.particles:
            x, y, theta = particle
            xSum += x
            ySum += y
            thetaSum += theta

        return (xSum/numberOfTuples, ySum/numberOfTuples, thetaSum/numberOfTuples)


    #function to find the nearest wall and the distance to it for ALL particles
    def update_nearest_walls(self,walls):
        self.nearest_wall = []
	self.distance_to_nearest_wall = []
        for i in xrange(len(self.particles)):
            wall_index, distance = self.get_wall_info(self.particles[i], walls)
            self.nearest_wall.append(wall_index)
            self.distance_to_nearest_wall.append(distance)

    #function to find the nearest wall and distance to it for ONE particle
    def get_wall_info(self, particle, walls):

        #NOTE that these values will be returned if no wall is found for particle
        nearest_wall_distance = 2000
        nearest_wall_index = -1

        for i in xrange(len(walls)):
            distance_from_wall = self.calculate_distance_from_wall(particle, walls[i])
            #check if the particle faces the wall
	    if (self.check_particle_faces_wall(particle, walls[i], distance_from_wall)):
                # If we find a smaller distance set it
                if(nearest_wall_distance > distance_from_wall):
                    nearest_wall_distance = distance_from_wall
                    nearest_wall_index = i

        return ( nearest_wall_index, nearest_wall_distance )


    #function to calculate the orthogonal distance from a particle to a wall
    def orthogonal_distance(self,particle,wall):
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

    #function to check that the measurement for ONE particle is safe
    def check_measurement_is_safe(self,particle_index,walls):
        nearest_wall_index = self.nearest_wall[particle_index]
        #measurement is not safe if there is no nearest wall
	if nearest_wall_index == -1:
		return False
        distance_to_wall = self.distance_to_nearest_wall[particle_index]
        short_distance_to_wall = self.orthogonal_distance(self.particles[particle_index], walls[nearest_wall_index])
        angle_with_wall = np.arccos(short_distance_to_wall/distance_to_wall)
        
        if(np.rad2deg(angle_with_wall) > 40):
            return False
        else:
            return True

    #function to calculate the distance of ONE particle to a given wall
    def calculate_distance_from_wall(self,particle, wall):
        x, y, theta = particle
        theta_rad = np.deg2rad(theta)
        a_x, a_y, b_x, b_y = wall
        numerator = (b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)
        denominator = (b_y - a_y)*math.cos(theta_rad) - (b_x - a_x)*math.sin(theta_rad)
        if(denominator == 0):
            # print 'Warning denominator was zero in calculate_distance_from_wall'
            return -sys.maxint
        return numerator/denominator

    #function which checks if x is in between x1 and x2
    def in_range(self,x, x1, x2):
        x_min = x1 if (x1 < x2) else x2
        x_max = x1 if (x1 > x2) else x2

        if(x_min <= x <= x_max):
            return True
        else:
            return False

    #function which checks if ONE particle faces a given wall - essentially if it can intersect with the wall
    def check_particle_faces_wall(self,particle,wall,m):
        """
        Note: edges cases like facing the corner of a wall return false
        """
        if(m < 0):
            return False
        x, y, theta = particle
        a_x, a_y, b_x, b_y = wall
        x_intersection = x + m*(np.cos(np.deg2rad(theta)))
        y_intersection = x + m*(np.sin(np.deg2rad(theta)))
        if (self.in_range(x_intersection,a_x, b_x) and self.in_range(y_intersection,a_y, b_y)):
            return True
        else:
            return False

    #function determine if an update using mcl is safe, according to particle cloud
    def update_is_safe(self, walls):
        self.safe_to_update = []
        trues = 0
        for i in xrange(len(self.particles)):
            self.safe_to_update.append(self.check_measurement_is_safe(i, walls))
        for i in xrange(len(self.safe_to_update)):
            if self.safe_to_update[i]:
                trues += 1
        if trues > len(self.particles)/2:
            return True
        else:
            print 'NOT SAFE', trues, '%'
            return False



#MAIN FUNCTIONS FOR MCL ALGORITHM#

    #function which updates weights
    def update_weights(self,walls,measurement):
        for i in xrange(len(self.particles)):
            #make sure that the distance_to_nearest wall is not 2000 (the default value)
            if distance_to_nearest_wall[i] != 2000:
                difference = self.distance_to_nearest_wall[i] - measurement
                likelihood = np.exp(-((difference)**2)/(2*self.sigma*self.sigma))
                self.weights[i] = self.weights[i]*likelihood
            #otherwise, don't update the weight, leave it as it is



    #function that normalises the weights of the particle cloud
    def normalize(self):
        sum = 0.0;
        for weight in self.weights:
            sum += weight
        if(sum != 0):
            for i in xrange(len(self.particles)):
                self.weights[i] = self.weights[i]/sum
        else:
            print "Warning! Particle weights got really small!"
            for i in xrange(len(self.particles)):
                self.weights[i] = 1.0/float(len(self.particles))

    #function which resamples using cumulative probability distribution
    def resample(self):
        """
        Resample N new particles with weight calculated using mcl with distribution
        determined by weight of particles
        """
        new_particles = []
        particles_count = len(self.particles)
        for i in xrange(particles_count):
            r = random.random()
            sum = 0
            for i in xrange(len(self.weights)):
                sum += self.weights[i]
                if (sum >= r):
                    #append particle for which r lies within its weight 
                    new_particles.append(self.particles[i])
                    break

        #reset the weights to (normalized) equal number
        for i in xrange(0,particles_count):
            self.weights[i] = 1.0/float(particles_count)

        self.particles = new_particles

 ###########END OF HELPER FUNCYIONS###############


 #MCL ALGORITHM
    def do_mcl(self,walls,measurement):
        #for each particle, finds the nearest wall and the distance to it.
        self.update_nearest_walls(walls)
        #determine if it is safe to update
        if self.update_is_safe(walls):
            self.update_weights(walls, measurement)
            self.normalize()
            self.resample()


#Movement functions, should use the ones from robot.py though#

    def left(self, deg):
        for i in range(len(self.particles)):
            x,y,theta = self.particles[i]
            g = random.gauss(0,0.2)
            self.particles[i] = (x, y, theta + deg + g)

    def forwards(self, cm):
        #update particle position after moving cm distance
        for i in range(len(self.particles)):
                x,y,theta = self.particles[i]
                e = random.gauss(0,1.6)
                f = random.gauss(0,0.2)

                self.particles[i] = ((x + (cm + e)*np.cos(np.deg2rad(theta))), (y + (cm + e)*np.sin(np.deg2rad(theta))), (theta + f))

"""
    TESTING
"""
"""
test = Particles()
# print test.temp((0,0,45,0),(-10,10,10,10))

test.particles[0] = (5,5,0,0.01)

print test.get_distance_to_nearest_wall(test.particles[0], walls)
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
print test.get_distance_to_nearest_wall(test.particles[0], walls)
test.forwards(2)
print test.particles
print test.get_distance_to_nearest_wall(test.particles[0], walls)
"""
