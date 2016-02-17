import random
import numpy as np
import time
import robot

c = 0;
sigmaX = sigmaY = 1.6
sigmaT = 0.2

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
                
                particles[i] = ((x + (cm + e)*np.cos(np.deg2rad(theta))), (y + (cm + e)*np.sin(np.deg2rad(theta))), (theta + f))
                nx,ny,ntheta = particles[i]
                if(i == 0):
                    line = (x, y, nx, ny)
                    print "drawLine:" + str(line)


#function to rotate particles deg degrees
def rotateParticles(deg):
        
        #update particle position after moving cm distance
        for i in range(numberOfParticles):
                x,y,theta = particles[i]
                
                f = getRandomTheta()

                particles[i] = (x, y, theta + deg + f)
        

#function to draw a square
def drawSquare(cm,move_robot=False):
        scaling_factor = 10
        for i in range(4):
                if(move_robot):
                    robot.forwards(cm)
                    robot.right(90)
                moveParticles(cm*scaling_factor) 
                rotateParticles(90)
                print "drawParticles:" + str(particles)

#drawSquare(50,False)
drawSquare(50,True)
