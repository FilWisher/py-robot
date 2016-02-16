import time
import sys
import random

c = 0;
sigmaX = sigmaY = 0.2
sigmaT = 0.01

def getRandomX():
	return random.gauss(0,sigmaX)

def getRandomY():
	return random.gauss(0,sigmaY)

def getRandomTheta(): 
	return random.gauss(0,sigmaT)

numberOfParticles = 100

#line1 = (10, 10, 10, 500) # (x0, y0, x1, y1)
#line2 = (20, 20, 500, 200)  # (x0, y0, x1, y1)

#print "drawLine:" + str(line1)
#print "drawLine:" + str(line2)

#initialise particles
particles = [(100,100,0) for i in range(numberOfParticles)]
print "drawParticles:" + str(particles)


#function to move particles straight
def moveParticles(cm):

        #update particle position after moving cm distance
        for i in range(numberOfParticles):
                x,y,theta = particles[i]
                e = getRandomX()
                f = getRandomTheta()

                particles[i] = [(x + (cm + e)*cos(deg2rad(theta))), (y + (cm + e)*sin(deg2rad(theta))), (theta + f)]


#function to rotate particles deg degrees
def rotateParticles(deg):
        
        #update particle position after moving cm distance
        for i in range(numberOfParticles):
                x,y,theta = particles[i]
                
                f = getRandomTheta()

                particles[i] = [(x), (y), (theta + deg + f)]
        

#function to draw a square
def drawSquare(cm):

        for i in range(4):
                moveParticles(100)
                rotateParticles(90)
                print "drawParticles:" + str(particles)
                print particles[0,2]

"""
while True:
	# Create a list of particles to draw. This list should be filled by tuples (x, y, theta).
	particles = [(getRandomX(), getRandomY(), getRandomTheta()) for i in range(numberOfParticles)]
	print "drawParticles:" + str(particles)
	
	c += 1;
	time.sleep(0.25)
"""
